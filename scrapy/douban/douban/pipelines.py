# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import openpyxl
import os

class DoubanPipeline:
    def __init__(self):
        self.wb = openpyxl.Workbook()
        self.ws = self.wb.active#获取活动表
        self.ws.append(['名称','出版信息','评分'])#添加表头
    def process_item(self, item, spider):
        #储存操作
        line = [item['title'], item['publish'], item['score']]
        #将列表数据添加到工作表中
        self.ws.append(line)

        return item
    def close_spider(self, spider):#储存并关闭方法
        filename = 'D:/Douban/'
        if not os.path.exists(filename):
            os.mkdir(filename)
        self.wb.save(filename + 'book.xlsx')
        self.wb.close()
