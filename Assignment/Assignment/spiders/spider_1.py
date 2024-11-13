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
        next_page = response.css('a[title="Next"]::attr(href)').get()
        if next_page:
            next_page_url = response.urljoin(next_page)
            yield scrapy.Request(next_page_url, callback=self.parse)
