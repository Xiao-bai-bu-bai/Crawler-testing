import scrapy
from tuxingren.items import TuxingrenItem

class YuansuSpider(scrapy.Spider):
    name = "yuansu"
    allowed_domains = ["txrpic.com"]
    start_urls = ["https://www.txrpic.com/png/"]

    def parse(self, response, **kwargs):
        a_hrefs = response.xpath('//div[@class="box data-info"]/div[1]/a/@href').extract()
        for a_href in a_hrefs:
            yield scrapy.Request(url=a_href, method='get', callback=self.parse_detail)

    def parse_detail(self, response, **kwargs):
        img_url = response.xpath('//div[@class="work-img-box"]/img/@src').extract_first()
        img_name = response.xpath('//div[@class="work-img-box"]/img/@title').extract_first()
        item = TuxingrenItem()
        item['img_url'] = img_url
        item['img_name'] = img_name
        yield item
