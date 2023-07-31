import requests
import os
from lxml import etree

filename = 'D:/novel/'
if not os.path.exists(filename):
    os.mkdir(filename)

html_url = 'https://www.qidian.com/rank/recom/'

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
}
response = requests.get(html_url, headers = headers).text
# print(response)
e = etree.HTML(response)

names = e.xpath("//div[@id='book-img-text']/ul/li/div[@class='book-mid-info']/h2/a/text()")
authers = e.xpath("//div[@id='book-img-text']/ul/li/div[@class='book-mid-info']/p[@class='author']/a[@class='name']/text()")
kinds = e.xpath("//div[@id='book-img-text']/ul/li/div[@class='book-mid-info']/p[@class='author']/a[@class='go-sub-type']/text()")
statuses = e.xpath("//div[@id='book-img-text']/ul/li/div[@class='book-mid-info']/p[@class='author']/span/text()")
# print(names, authers)

for name, auther, kind, statuse, in zip(names, authers, kinds, statuses):
    print('书名:{} --- 作者:{} --- 类别:{} --- 状态:{}'.format(name, auther, kind, statuse))