import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from scrapy.http import HtmlResponse
import time


class spider_1(scrapy.Spider):
    name = 'spider_1'
    start_urls = [
        'https://www.bayut.com/to-rent/property/dubai/'
    ]

    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        driver_path = "C:\Program Files (x86)\chromedriver.exe"
        service = Service(driver_path)
        self.driver = webdriver.Chrome(service=service, options=chrome_options)

    def parse(self, response):
        link = response.css('a.d40f2294[aria-label="Listing link"]::attr(href)').extract()
        for links in link:
            absolute_url = response.urljoin(links)
            yield response.follow(absolute_url, callback=self.parse_item)
        next_page = response.css('a[title="Next"]::attr(href)').get()
        if next_page:
            next_page_url = response.urljoin(next_page)
            yield scrapy.Request(next_page_url, callback=self.parse)

    def parse_item(self, response):
        self.driver.get(response.url)
        time.sleep(1)  # Wait for JavaScript to load (adjust as needed)

        # Get the rendered HTML and wrap it in a Scrapy response
        rendered_html = self.driver.page_source
        response = HtmlResponse(url=response.url, body=rendered_html, encoding='utf-8')

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
            'agent_name': response.css(
                'a[aria-label="Agent name"] h2::text, span[aria-label="Agent name"]::text').get(),
            'primary_image_url': response.css('img._4a3dac18[aria-label="Cover Photo"]::attr(src)').get(),
            'breadcrumbs': " > ".join(response.css('a.ebd56459 span._43ad44d9::text').extract()),
            'amenities': response.css('span._7181e5ac::text').extract(),
            'description': "".join(response.css('span._3547dac9 *::text').getall()),
            'property_image_urls': response.css('img._5a31e77d.e6a91003[role="presentation"]::attr(src)').extract()
        }

    def closed(self, reason):
        self.driver.quit()
