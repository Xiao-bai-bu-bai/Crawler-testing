import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from qiche.items import QicheItem


class ErshouSpider(CrawlSpider):
    name = "ershou"
    allowed_domains = ["che168.com"]
    start_urls = ["https://www.che168.com/shangqiu/a0_0msdgscncgpi1ltocsp1exx0/"]

    rules = (
        Rule(LinkExtractor(
            deny='https://topicm.che168.com/TopicApp/2021/businessregistrationrevision/index?lmnt=https%3A%2F%2Fdspmnt.autohome.com.cn%2Fmonitor%3Frtype%3D4%26axd%3D1%26clickid%3Da6a4be19-1370-48e0-a7d0-650c7d230318%26&from=1&pvareaid=110644',
            restrict_xpaths='//div[@class="tp-cards-tofu fn-clear"]/ul/li/a'),
             callback="parse_item", follow=False),
        Rule(LinkExtractor(restrict_xpaths='//div[@class="page fn-clear"]/a[@class="page-item-next"]'), follow=True)
    )

    def parse_item(self, response):
        # print(response.url)
        title = response.xpath('//h3[@class="car-brand-name"]/text()').extract_first()
        title = title.strip() if title else None
        price = response.xpath('//div[@class="brand-price-item"]/span/text()').extract_first()
        archives = response.xpath('//h3[@class="all-title"]/text()').extract_first()
        span_list = response.xpath('//ul[@class="basic-item-ul"]/li/span/text()').extract()
        li_list = response.xpath('//ul[@class="basic-item-ul"]/li/text()').extract()
        li_list = li_list[:-1]
        # span_list = [i.replace('\xa0', '') for i in span_list]
        if title:
            car = QicheItem()
            car["title"] = title
            car["price"] = price
            car["archives"] = archives
            car["span_list"] = span_list
            car["li_list"] = li_list
            print(title)
            yield car
