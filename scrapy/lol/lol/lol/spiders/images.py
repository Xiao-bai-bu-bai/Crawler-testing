import scrapy
from lol.items import LolItem


class ImagesSpider(scrapy.Spider):
    name = "images"
    allowed_domains = ["leagueoflegends.com"]
    start_urls = ["https://www.leagueoflegends.com/zh-tw/champions/"]

    def parse(self, response, **kwargs):
        hero_urls = response.xpath('//div[@class="style__List-sc-13btjky-2 IorQY"]/a/@href').extract()
        for hero_url in hero_urls:
            hero_url = response.urljoin(hero_url)
            yield scrapy.Request(url=hero_url, method='get', callback=self.parse_detail)

    def parse_detail(self, response, **kwargs):
        img_url = response.xpath('//div[@class="style__SlideshowItemImage-sc-gky2mu-4 bRtALz"]/img/@src').extract()
        item = LolItem()
        img_name = response.xpath('//div[@class="swiper-wrapper"]/li/button/label/text()').extract()
        item['img_name'] = img_name
        item['img_url'] = img_url
        yield item
