import scrapy
from bs4 import BeautifulSoup
from ..items import DoubanItem

class DoubanSpider(scrapy.Spider):
    name = 'douban'#定义爬虫的名称，在start中使用
    allowed_domains = ['book.douban.com/top250']#允许爬虫的域名
    start_urls = ['https://book.douban.com/top250']#爬虫的起始网址

#parse是父类中的处理response响应的一个方法
    def parse(self,response):
        bs = BeautifulSoup(response.text, 'html.parser')
        tr_tag = bs.find_all('tr', class_='item')
        for tr in tr_tag:
            item = DoubanItem()#创建对象
            title = tr.find_all('a')[1]['title']#提取书名
            publish = tr.find('p', class_="pl").text#提取出版信息
            score = tr.find('span', class_="rating_nums").text#提取评分
            # print([title,publish,score])
            item['title'] = title
            item['publish'] = publish
            item['score'] = score
            #封装完成之后提交给引擎
            yield item
