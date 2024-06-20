# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class BaiduwenkuPipeline:
    def open_spider(self, spider):
        print("爬虫开始")
        self.f = open("baiqi.txt", "a", encoding="utf-8")

    def close_spider(self, spider):
        if self.f:
            self.f.close()
        print("爬虫结束")

    def process_item(self, item, spider):
        self.f.write(item["title"] + "\n")
        self.f.write(item["posts"] + "\n")
        self.f.write(item["substance"] + "\n")
        return item

