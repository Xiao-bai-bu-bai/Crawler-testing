# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
from scrapy.pipelines.images import ImagesPipeline
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class LolPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        for img_url, img_name in zip(item['img_url'], item['img_name']):
            request = scrapy.Request(img_url)
            request.meta['img_name'] = img_name  # 将图片名称添加到请求的meta中
            yield request

    def file_path(self, request, response=None, info=None, item=None):
        hero_name = item['img_name']
        print(hero_name)
        return f'{hero_name[0]}/{request.meta["img_name"]}.jpg'  # 从请求的meta中取出图片名称

    def item_completed(self, results, item, info):
        pass
