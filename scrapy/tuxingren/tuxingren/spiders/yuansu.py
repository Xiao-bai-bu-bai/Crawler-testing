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
            break

        # 获取下一页的url，判断是否为下一页
        next_page = response.xpath('//div[@class="main-page-box"]/a[contains(text(), "下一页")]/@href').extract_first()
        #  拼接完整的url
        next_page = response.urljoin(next_page)
        print(next_page)

        #  判断是否为下一页
        if next_page:
            yield scrapy.Request(next_page, callback=self.parse)



    def parse_detail(self, response, **kwargs):
        img_url = response.xpath('//div[@class="work-img-box"]/img/@src').extract_first()
        img_name = response.xpath('//div[@class="work-img-box"]/img/@title').extract_first()
        item = TuxingrenItem()
        item['img_url'] = img_url
        item['img_name'] = img_name
        yield item
