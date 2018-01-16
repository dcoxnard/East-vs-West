import scrapy


class ZeitungSpider(scrapy.Spider):

    name = 'sueddeutsche_zeitung_spider'

    custom_settings = {
        "DOWNLOAD_DELAY": 3,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 3,
        # "HTTPCACHE_ENABLED": True
    }

    start_urls = [
        'http://www.sueddeutsche.de/'
    ]

    def parse(self, response):

        a = response.xpath('//div[contains(@class,"teaser")]/p/@data-clickable').extract()
        stem = 'http://www.sueddeutsche.de'
        hrefs = [i.split('=')[-1].strip("']") for i in a]

        for href in hrefs:

            section = href.split('/')[3]
            article_id = href.split('-')[-1]



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

        article_headline = response.xpath('//h2/text()').extract()[1].strip()

        date = response.xpath('//time/text()').extract_first().strip()

        # Contains a list of mostly whitespace -- fix later.  Maybe by searching for Title Case?
        author = response.xpath('//div[@class="authorProfileContainer"]//text()').extract()

        article_text = response.xpath('//section[@id="article-body"]/p/text()').extract()

        yield {
            'url': url,
            'article_id': article_id,
            'section': section,
            'article_headline': article_headline,
            'date': date,
            'author': author,
            'article_text': article_text,
            }




