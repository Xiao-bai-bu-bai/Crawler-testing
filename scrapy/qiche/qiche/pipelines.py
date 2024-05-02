# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class QichePipeline:
    '''
    保存数据到csv文件
    执行过程：
    首先执行open_spider方法，打开文件
    然后执行process_item方法，将数据写入文件
    最后执行close_spider方法，关闭文件
    '''

    def open_spider(self, spider):
        print("爬虫开始")
        self.f = open("ershou.csv", "a", encoding="utf-8")
        self.f.write(
            "名称,价格(万),上牌时间,表显里程,变速箱,排放标准,排量,发布时间,年检到期,保险到期,质保到期,过户次数,所在地,发动机,车辆级别,车身颜色,燃油标号,驱动方式\n"
        )

    def close_spider(self, spider):
        if self.f:
            self.f.close()
        print("爬虫结束")

    def process_item(self, item, spider):
        self.f.write(item["title"] + ",")
        self.f.write(item["price"] + ",")
        for li in item["li_list"]:
            self.f.write(li + ",")
        self.f.write("\n")
        print(f'{item["title"]}，数据保存成功！')
        return item
