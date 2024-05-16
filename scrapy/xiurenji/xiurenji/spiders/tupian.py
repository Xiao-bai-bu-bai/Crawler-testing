import scrapy
from xiurenji.items import XiurenjiItem


class TupianSpider(scrapy.Spider):
    name = "tupian"
    allowed_domains = ["123783.xyz"]
    start_urls = ["https://www.123783.xyz/MFStar/"]

    def parse(self, response, **kwargs):
        cover_urls = response.xpath('//div[@class="update_area_content"]/ul/li/a/@href').extract()
        cover_names = response.xpath('//div[@class="update_area_content"]/ul/li/a/@alt').extract()

        #  拼接完整的url
        for cover_url, cover_name in zip(cover_urls, cover_names):
            cover_url = response.urljoin(cover_url)
            yield scrapy.Request(url=cover_url, method='get', callback=self.parse_cover,
                                 meta={'cover_name': cover_name})

        # 获取下一页的url，判断是否为下一页
        next_page = response.xpath('//div[@class="page"]/a[contains(text(), "下页")]/@href').extract_first()
        #  拼接完整的url
        next_page = response.urljoin(next_page)

        #  判断是否为下一页
        if next_page:
            yield scrapy.Request(next_page, callback=self.parse)

    def parse_cover(self, response, **kwargs):

        #  获取图片的url
        image_urls = response.xpath('//div[@class="content"]/p/img/@src').extract()
        cover_name = response.meta['cover_name']

        for image_url in image_urls:
            image_url = response.urljoin(image_url)
            yield scrapy.Request(url=image_url, method='get', callback=self.parse_image,
                                 meta={'cover_name': cover_name})

         # 获取下一页的url，判断是否为下一页
        next_page = response.xpath('//div[@class="page"]/a[contains(text(), "下页")]/@href').extract_first()
        #  拼接完整的url
        next_page = response.urljoin(next_page)

        #  判断是否为下一页
        if next_page:
            yield scrapy.Request(next_page, callback=self.parse_cover, meta={'cover_name': cover_name})

    def parse_image(self, response, **kwargs):
        item = XiurenjiItem()
        item['cover_name'] = response.meta['cover_name']
        item['img_url'] = response.url
        yield item
