# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class Tianya2Pipeline:
    def open_spider(self, spider):
        print("爬虫开始")
        self.f = open("tianya.csv", "a", encoding="utf-8")
        self.f.write("作者,发布的内容\n")

    def close_spider(self, spider):
        if self.f:
            self.f.close()
        print("爬虫结束")

    def process_item(self, item, spider):
        self.f.write(item["author"] + ",")
        self.f.write("".join(item["content"]) + "\n")
        print('爬取成功', item['author'])
        return item
