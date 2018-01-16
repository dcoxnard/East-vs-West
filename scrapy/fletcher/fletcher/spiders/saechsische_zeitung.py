import scrapy


class ZeitungSpider(scrapy.Spider):

    name = 'saechsische_zeitung_spider'

    custom_settings = {
        "DOWNLOAD_DELAY": 3,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 3,
        # "HTTPCACHE_ENABLED": True
    }

    start_urls = [
        'http://www.sz-online.de/'
    ]

    def parse(self, response):

        hrefs = response.xpath('//div[contains(@id, "szoMainColumn")]//'\
            'article//a/@href').extract()
        stem = 'http://www.sz-online.de'
        hrefs = [stem + href for href in hrefs]

        for href in hrefs:

            section = href.split('/')[3]
            article_id = href.split('-')[-1].split('.')[0]

            yield scrapy.Request(
                url=href,
                callback=self.parse_story,
                meta={'url': href,
                      'section': section,
                      'article_id': article_id,
                }
            )


    def parse_story(self, response):

        url = response.request.meta['url']

        section = response.request.meta['section']

        article_id = response.request.meta['article_id']

        article_headline = response.xpath('//h1/text()').extract()[1].strip()

        date = response.xpath('//span[contains(@class, "szoPubDate")]/text()').extract()[1].strip()

        # Author has a "Von" that I can't get rid of.  Fix in the pandas stage.
        author = response.xpath('//p[contains(@class, "szoAuthor")]/text()').extract_first()
        if author:
            author = ' '.join(author.split()[1:])

        # Some annoying whitespace in here.
        article_text = response.xpath('//article[contains(@class, "szoArticleView")]/p/text()').extract()

        yield {
            'url': url,
            'article_id': article_id,
            'section': section,
            'article_headline': article_headline,
            'date': date,
            'author': author,
            'article_text': article_text,
            }



