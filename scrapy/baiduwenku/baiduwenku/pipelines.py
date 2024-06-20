# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from baiduwenku.settings import MySql
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class BaiduwenkuPipeline:
    pass
    # 保存为txt文件
    # def open_spider(self, spider):
    #     print("爬虫开始")
    #     self.f = open("baiqi.txt", "a", encoding="utf-8")
    #
    # def close_spider(self, spider):
    #     if self.f:
    #         self.f.close()
    #     print("爬虫结束")
    #
    # def process_item(self, item, spider):
    #     self.f.write(item["title"] + "\n")
    #     self.f.write(item["posts"] + "\n")
    #     self.f.write(item["substance"] + "\n")
    #     return item

    # 保存到数据库
class BaiduMysqlPipeline:
    '''
    保存数据到数据库
    执行过程：
    首先执行open_spider方法，打开数据库连接
    然后执行process_item方法，将数据写入数据库
    最后执行close_spider方法，关闭数据库连接
    '''

    def open_spider(self, spider):
        print("爬虫开始")
        self.conn = pymysql.connect(
            host=MySql["host"],
            port=MySql["port"],
            user=MySql["user"],
            password=MySql["password"],
            database=MySql["database"],
        )

    def close_spider(self, spider):
        if self.conn:
            self.conn.close()
        print("爬虫结束")

    def process_item(self, item, spider):
        try:
            cursor = self.conn.cursor()  # 获取游标
            sql = "insert into baiduwenku (title, posts, substance) values(%s, %s, %s)"
            cursor.execute(sql, (item["title"], item["posts"], item["substance"]))
            self.conn.commit()
        except:
            self.conn.rollback()
        finally:
            if cursor:
                cursor.close()
        return item

