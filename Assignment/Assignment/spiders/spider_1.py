import scrapy


class spider_1(scrapy.Spider):
    name = 'spider_1'
    start_urls = [
        'https://www.bayut.com/to-rent/property/dubai/'
    ]

    def parse(self, response):
        for rooms in response.css("li.a37d52f0"):
            yield {
                'location': rooms.css('h3._4402bd70::text').extract(),
                'type': rooms.xpath('.//span[@class="_19e94678 e0abc2de" and @aria-label="Type"]/text()').extract(),
                'links': rooms.css('a.d40f2294').attrib['href'],
            }
        next_page = response.css('a._95dd93c1').attrib['href']
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
