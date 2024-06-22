# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline


class TuxingrenPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        img_url = item['img_url']
        request = scrapy.Request(img_url)
        yield request

    def file_path(self, request, response=None, info=None, item=None):
        img_name = item['img_name']
        kind_name = item['kind_name']
        print(img_name)
        return f'{kind_name}\\{img_name}.jpg'  # 从请求的meta中取出图片名称

    def item_completed(self, results, item, info):
        pass
