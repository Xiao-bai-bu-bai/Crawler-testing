import scrapy
from scrapy.linkextractors import LinkExtractor


class ErshoucheSpider(scrapy.Spider):
    name = "ershouche"
    allowed_domains = ["che168.com"]
    start_urls = ["https://www.che168.com/shangqiu/list/#pvareaid=100945"]

    def parse(self, response, **kwargs):
        # hrefs = response.xpath('//div[@class="tp-cards-tofu fn-clear"]/ul/li/a/@href').extract()
        # print(hrefs)
        # for href in hrefs[:-1]:
        #     url = response.urljoin(href)
        #     yield scrapy.Request(url, callback=self.parse_detail)
        # 使用链接提取器提取链接
        le = LinkExtractor(restrict_xpaths='//div[@class="tp-cards-tofu fn-clear"]/ul/li/a')
        links = le.extract_links(response)  # 提取所有的链接
        for link in links:
            yield scrapy.Request(link.url, callback=self.parse_detail)

        # 提取下一页链接
        link_le = LinkExtractor(restrict_xpaths='//div[@class="page fn-clear"]/a/')
        page_links = link_le.extract_links(response)
        for page_link in page_links:
            yield scrapy.Request(page_link.url, callback=self.parse)


    def parse_detail(self, response):
        print(response.url)
        # title = response.xpath('//h3/text()').extract_first().strip()
        # price = response.xpath('//div[@class="car-price"]/span/text()').extract_first()

        # next_page = response.xpath('//a[@class="page-item-next"]/@href').extract_first()
        # if next_page:
        #     next_url = response.urljoin(next_page)
        #     yield scrapy.Request(next_url, callback=self.parse)
