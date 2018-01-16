import scrapy


class ZeitungSpider(scrapy.Spider):

    name = 'leipziger_volkszeitung_spider'

    custom_settings = {
        "DOWNLOAD_DELAY": 3,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 3,
        # "HTTPCACHE_ENABLED": True
    }

    start_urls = [
        'http://www.lvz.de/'
    ]

    def parse(self, response):

        hrefs = response.xpath(
        	'//div[contains(@class, "pda-left")]//'\
        	'div[contains(@class, "pda-depblock-content-headline")]//@href'
        ).extract()
        stem = 'http://www.lvz.de/'
        hrefs = [stem + href for href in hrefs]

        for href in hrefs:

            section = href.split('/')[5]
            article_id = href.split('/')[4]

            yield scrapy.Request(
                url=href,
                callback=self.parse_story,
                meta={'url': href,
                      'section': section,
                      'article_id': None
                }
            )


    def parse_story(self, response):

        url = response.request.meta['url']

        section = response.request.meta['section']

        article_id = response.request.meta['article_id']

        article_headline = response.xpath('//h1/text()').extract_first().strip()

        date = response.xpath('//span[contains(@itemprop, "datepublished")]/@content').extract_first()

        author = response.xpath('//span[contains(@itemprop, "author")]/text()').extract_first()

        ### Lots of gross whitespace, will probabably need to strip when concat'ing in pandas.
        article_text = response.xpath('//div[contains(@id, "articlecontent")]//p/text()').extract()

        yield {
            'url': url,
            'article_id': article_id,
            'section': section,
            'article_headline': article_headline,
            'date': date,
            'author': author,
            'article_text': article_text,
            }



