import scrapy
from tuxingren.items import TuxingrenItem

class YuansuSpider(scrapy.Spider):
    name = "yuansu"
    allowed_domains = ["txrpic.com"]
    start_urls = ["https://www.txrpic.com/"]

    def parse(self, response, **kwargs):
        # 提取所有分类的url和名称
        url_kind = response.xpath('//div[@class="left-side"]/ul/li//a/@href').extract()
        kind_name = response.xpath('//div[@class="left-side"]/ul/li//a/text()').extract()

        for url, kind_name in zip(url_kind, kind_name):
                    url = response.urljoin(url)
                    yield scrapy.Request(url=url, method='get', callback=self.parse_kind, meta={'kind_name': kind_name})

    def parse_kind(self, response, **kwargs):
        # 提取分类下的所有图片的url
        a_hrefs = response.xpath('//div[@class="box data-info"]/div[1]/a/@href').extract()
        kind_name = response.meta['kind_name']
        for a_href in a_hrefs:
            yield scrapy.Request(url=a_href, method='get', callback=self.parse_detail, meta={'kind_name': kind_name})

        # 获取下一页的url，判断是否为下一页
        next_page = response.xpath('//div[@class="main-page-box"]/a[contains(text(), "下一页")]/@href').extract_first()
        #  拼接完整的url
        next_page = response.urljoin(next_page)

        #  判断是否为下一页
        if next_page:
            yield scrapy.Request(next_page, callback=self.parse_kind)



    def parse_detail(self, response, **kwargs):
        # 提取图片的url和名称
        img_url = response.xpath('//div[@class="work-img-box"]/img/@src').extract_first()
        img_name = response.xpath('//div[@class="work-img-box"]/img/@title').extract_first()
        kind_name = response.meta['kind_name']
        item = TuxingrenItem()
        item['img_url'] = img_url
        item['img_name'] = img_name
        item['kind_name'] = kind_name
        yield item
