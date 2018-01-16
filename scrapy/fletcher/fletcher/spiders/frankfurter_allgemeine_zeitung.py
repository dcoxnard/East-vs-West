import scrapy


class ZeitungSpider(scrapy.Spider):

    name = 'frankfurter_allgemeine_zeitung_spider'

    custom_settings = {
        "DOWNLOAD_DELAY": 3,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 3,
        # "HTTPCACHE_ENABLED": True
    }

    start_urls = [
        'http://www.faz.net/aktuell/'
    ]

    def parse(self, response):

        hrefs = response.xpath('//*[@id="TOP"]/div[@class="Home "]//a[contains(@class, "tsr-Base_ContentLink")]/@href').extract()
        stem = 'http://www.faz.net'
        hrefs = [stem + href for href in hrefs]

        for href in hrefs:

            section = href.split('/')[4]
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

        article_headline = response.xpath('//span[@class="atc-HeadlineText"]/text()').extract_first().strip()

        date = response.xpath('//time/text()').extract_first().strip()

        author = response.xpath('//a[@class="atc-MetaAuthorLink"]/span/text()').extract_first().strip()

        # Combine elements b/c first letter of article is in its own tag.
        article_text = response.xpath('//div[@class=" atc-Text"]/p/text()').extract()
        first_letter = response.xpath('//div[@class=" atc-Text"]/p/span/text()').extract_first().strip()
        article_text[0] = first_letter + article_text[0]

        yield {
            'url': url,
            'article_id': article_id,
            'section': section,
            'article_headline': article_headline,
            'date': date,
            'author': author,
            'article_text': article_text,
            }



