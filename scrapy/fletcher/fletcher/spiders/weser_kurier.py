import scrapy


class ZeitungSpider(scrapy.Spider):

    name = 'weser_kurier_spider'

    custom_settings = {
        "DOWNLOAD_DELAY": 3,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 3,
        # "HTTPCACHE_ENABLED": True
    }

    start_urls = [
        'https://www.weser-kurier.de/'
    ]

    def parse(self, response):

        hrefs1 = response.xpath('//section[contains(@class, "nfy-topbox-container")]//@href').extract()
        hrefs2 = response.xpath('//div[contains(@class, "direct_content")]//a[contains(@class, "article_headline")]/@href').extract()
        hrefs = hrefs1 + hrefs2
        stem = 'https://www.weser-kurier.de'
        hrefs = [stem + href for href in hrefs]

        for href in hrefs:

            section = href.split('/')[3]
            article_id = href.split(',')[-1].split('.')[0]

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

        article_headline = response.xpath('//h1/text()').extract_first()

        date = response.xpath('//span[contains(@class, "authors-date")]/text()').extract_first()

        author = response.xpath('//span[contains(@itemprop, "name")]/text()').extract_first()

        article_text = response.xpath('//div[contains(@id, "onlineText")]//p/text()').extract()

        yield {
            'url': url,
            'article_id': article_id,
            'section': section,
            'article_headline': article_headline,
            'date': date,
            'author': author,
            'article_text': article_text,
            }



