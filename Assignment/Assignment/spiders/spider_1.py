import scrapy


class spider_1(scrapy.Spider):
    name = 'spider_1'
    start_urls = [
        'https://www.bayut.com/to-rent/property/dubai/'
    ]

    def parse(self, response):
        # item_links = response.css('a.d40f2294::attr(href)').getall()
        # for items in item_links:
        #     yield response.follow(items, callback=self.parse)
        link = response.css('a.d40f2294[aria-label="Listing link"]::attr(href)').extract()
        for links in link:
            absolute_url = response.urljoin(links)
            yield response.follow(absolute_url, callback=self.parse_item)
        next_page = response.css('a[title="Next"]::attr(href)').get()
        if next_page:
            next_page_url = response.urljoin(next_page)
            yield scrapy.Request(next_page_url, callback=self.parse)

    def parse_item(self, response):
        # for rooms in response.css("li.a37d52f0"):
        #     yield {
        #         'location': rooms.css('h3._4402bd70::text').extract(),
        #         'type': rooms.xpath('.//span[@class="_19e94678 e0abc2de" and @aria-label="Type"]/text()').extract(),
        #         'links': rooms.css('a.d40f2294').attrib['href'],
        #     }

        yield {
            'property_id': response.css('span._2fdf7fc5[aria-label="Reference"]::text').get(),
            'property_url': response.url,
            'purpose': response.css('span._2fdf7fc5[aria-label="Purpose"]::text').get(),
            'type': response.css('span._2fdf7fc5[aria-label="Type"]::text').get(),
            'added_on': response.css('span._2fdf7fc5[aria-label="Reactivated date"]::text').get(),
            'furnishing': response.css('span._2fdf7fc5[aria-label="Furnishing"]::text').get() or 'NA',
            'price': {
                'currency': response.css('span.d241f2ab[aria-label="Currency"]::text').get(),
                'amount': response.css('span._2d107f6e[aria-label="Price"]::text').get()
            },
            'location': response.css('div.e4fd45f0[aria-label="Property header"]::text').get(),
            'bed_bath_size': {
                'bedrooms': response.css('span._783ab618[aria-label="Beds"] span::text').get(),
                'bathrooms': response.css('span._783ab618[aria-label="Baths"] span::text').get(),
                'size': response.css('span[aria-label="Area"] span._140e6903 span::text').get()
            },
            'permit_number': response.css('span.e56292b8[aria-label="Permit Number"]::text').get(),
            'agent_name': response.css('a[aria-label="Agent name"] h2::text, span[aria-label="Agent name"]::text').get(),
            'primary_image_url':  response.css('img._4a3dac18[aria-label="Cover Photo"]::attr(src)').get(),
            'breadcrumbs':  " > ".join(response.css('a.ebd56459 span._43ad44d9::text').extract()),
            'amenities': response.css('span._7181e5ac::text').extract(),
            'description': "".join(response.css('span._3547dac9 *::text').getall()),
            'property_image_urls': response.css('img._5a31e77d.e6a91003[role="presentation"]::attr(src)').extract()
        }