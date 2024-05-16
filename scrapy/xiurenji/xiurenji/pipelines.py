# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import scrapy
from scrapy.pipelines.images import ImagesPipeline


class XiurenjiPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        img_url = item['img_url']

        request = scrapy.Request(img_url)
        yield request

    def file_path(self, request, response=None, info=None, item=None):
        cover_name = item['cover_name']
        img_name = request.url.split('/')[-1]
        print(cover_name, img_name)
        return f'{cover_name}/{img_name}'  # 从请求的meta中取出图片名称

    def item_completed(self, results, item, info):
        pass
