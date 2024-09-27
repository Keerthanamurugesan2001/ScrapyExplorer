import scrapy
from chocolatescraper.items import ChocolateProductItem
from chocolatescraper.item_loader import ChocolateProductItemLoader
from urllib.parse import urlencode

API_KEY = 'Enter your api key here'


def get_proxy_url(url):
    payload = {'api_key': API_KEY, 'url': url}
    print(urlencode(payload))
    proxy_url = 'https://proxy.scrapeops.io/v1/?' + urlencode(payload)
    print(proxy_url)
    return proxy_url

class ChocolateItemloaderSpider(scrapy.Spider):
    name = "chocolate_itemloader"
    # allowed_domains = ["chocolate.co.uk"]
    # start_urls = ['https://www.chocolate.co.uk/collections/all']
    
    def start_requests(self):
        start_url = 'https://www.chocolate.co.uk/collections/all'
        yield scrapy.Request(url=start_url, callback=self.parse)


    def parse(self, response):
        products = response.css('product-item')
        
        for product in products:
            chocolate = ChocolateProductItemLoader(item=ChocolateProductItem(), selector=product)
            chocolate.add_css('name', "a.product-item-meta__title::text")
            chocolate.add_css('price', 'span.price', re='<span class="price">\n              <span class="visually-hidden">Sale price</span>(.*)</span>')
            chocolate.add_css('url', 'div.product-item-meta a::attr(href)')
            yield chocolate.load_item()
        next_page = response.css('[rel="next"] ::attr(href)').get()

        if next_page is not None:
            next_page_url = 'https://www.chocolate.co.uk' + next_page
            yield response.follow(url=next_page_url, callback=self.parse)

    
