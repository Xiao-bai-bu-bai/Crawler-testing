import requests
from lxml import etree
import os

#保存路径
filename = 'D:\wallpaper\\'
if not os.path.exists(filename):
    os.mkdir(filename)

#爬取资源路径
html_url = 'https://yys.163.com/media/picture.html'

#伪装自己
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.183'
}

#获取资源
response = requests.get(html_url, headers = headers).text
# print(response)

#转变格式
e = etree.HTML(response)

#获取图片资源
list_url =[i[:i.rindex('/')] + '/1920x1080.jpg' for i in e.xpath('//div[@class="tab-cont"]/div/div/img/@data-src')]
# print(list_url)

#遍历下载每个资源
for i in list_url:
    wallpaper_coutent = requests.get(i , headers = headers).content
    name = i[i.index('picture'):i.rindex('/')].replace('/', '-')
    with open(filename + name + '.jpg', mode='wb') as f:
        f.write(wallpaper_coutent)
    print(name)