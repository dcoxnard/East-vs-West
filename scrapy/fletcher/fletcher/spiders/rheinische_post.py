import scrapy


class ZeitungSpider(scrapy.Spider):

    name = 'rheinische_post_spider'

    custom_settings = {
        "DOWNLOAD_DELAY": 3,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 3,
        # "HTTPCACHE_ENABLED": True
    }

    start_urls = [
        'http://www.rp-online.de'
    ]

    def parse(self, response):

        hrefs = response.xpath('//article[@data-vr-contentbox]//a/@href').extract()
        stem = 'http://www.rp-online.de'
        hrefs = [stem + href for href in hrefs]

        for href in hrefs:

            section = href.split('/')[3]
            article_id = href.split('.')[-1]

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

        article_headline = response.xpath('//h2/div[@class="headline"]//text()').extract_first()

        date = response.xpath('//time/@datetime').extract_first()

        author = response.xpath('//span[@class="author"]//text()').extract_first()

        article_text = response.xpath('//div[contains(@class, "main-text")]/p/text()').extract()

        yield {
            'url': url,
            'article_id': article_id,
            'section': section,
            'article_headline': article_headline,
            'date': date,
            'author': author,
            'article_text': article_text,
            }



