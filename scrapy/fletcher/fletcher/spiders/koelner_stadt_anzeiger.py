import scrapy


class ZeitungSpider(scrapy.Spider):

    name = 'koelner_stadt_anzeiger_spider'

    custom_settings = {
        "DOWNLOAD_DELAY": 3,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 3,
        # "HTTPCACHE_ENABLED": True
    }

    start_urls = [
        'https://www.ksta.de/'
    ]

    def parse(self, response):

        hrefs = [i for i in  response.xpath('//article[contains(@class, "dm")]//@href').extract() if i != 'javascript:']
        stem = 'https://www.ksta.de'
        hrefs = [stem + href for href in hrefs]

        for href in hrefs:

            section = href.split('/')[1]
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

        article_headline_strong = response.xpath('//h2/strong/text()').extract_first()

        article_headline_normal = response.xpath('//h2/text()').extract()[1].strip()

        date = response.xpath('//time/text()').extract_first().strip()

        author = response.xpath('//li[contains(@class, "dm_article_author")]/span/text()').extract_first()

        article_text = response.xpath('//div[contains(@class, "dm_article_text")]/p/text()').extract()

        yield {
            'url': url,
            'article_id': article_id,
            'section': section,
            'article_headline_strong': article_headline_strong,
            'article_headline_normal': article_headline_normal,
            'date': date,
            'author': author,
            'article_text': article_text,
            }



