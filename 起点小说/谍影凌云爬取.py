import requests
import os
import re
from lxml import etree
#文件保存路径
filename = 'D:/novel/谍影凌云/'
if not os.path.exists(filename):
    os.mkdir(filename)
#网页路径
html_url = 'https://www.qidian.com/ajax/book/category?bookId=1034379627&_csrfToken=On1HjlGqRnphw35fJ8NVpz4alXyWosfGAECbVIEM'
#伪装user_agent为浏览器，referer是从哪个网页跳转的，cookie记录网站的记录
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    'Referer':'https://www.qidian.com/book/1034379627/',
    'Cookie':'_csrfToken=On1HjlGqRnphw35fJ8NVpz4alXyWosfGAECbVIEM; trkf=1; supportWebp=true; supportwebp=true; qdrs=0%7C3%7C0%7C0%7C1; navWelfareTime=1690548324957; showSectionCommentGuide=1; qdgd=1; rcr=1034379627; bc=1034379627; _yep_uuid=eea0d9d5-fec5-f759-7fcb-ae81ff19f7ef; lrbc=1034379627%7C728045438%7C0; newstatisticUUID=1690549541_85278767; fu=569587450; traffic_utm_referer=https%3A//www.baidu.com/link; e2=%7B%22l6%22%3A%22%22%2C%22pid%22%3A%22qd_p_qidian%22%2C%22eid%22%3A%22%22%2C%22l1%22%3A2%7D; e1=%7B%22l6%22%3A%22%22%2C%22pid%22%3A%22qd_p_qidian%22%2C%22eid%22%3A%22qd_H_Search%22%2C%22l1%22%3A2%7D'

}
#提取网址内容并通过正则化提取每章的id
response = requests.get(html_url, headers = headers)
response.encoding = 'gzip'
# print(response.text)
list_id = re.findall(',"id":(\d+),"sS":1}', response.text)
# print(list_id)

#跳转到每章后提取文字整合为一篇文章，最后保存
for i, j  in zip(list_id, range(len(list_id))):
    novel_url = f'https://www.qidian.com/chapter/1034379627/{i}/'
    response = requests.get(novel_url, headers = headers).text
    text1 = re.findall('\u003cp>　　(.*)\u003cp>', response)[0]
    e = etree.HTML(response)
    name = (str(j) + str(e.xpath('//div[@class="relative"]/div/h1/text()')))
    text1 = text1.replace('</p><p>　　', '\n')
    with open(filename + name + '.text', mode = 'w') as f:
        f.write(text1)
    print(name)


    # e = etree.HTML(response)
    # text = e.xpath("//div[@class='print <sm:pt-56px <sm:mb-48px <sm:px-20px pt-64px px-64px mb-64px enable-review']")
    # print(text)

# headers = {
#     'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
# }
#
# novel_url = f'https://www.qidian.com/chapter/1034379627/718905313/'
# response = requests.get(novel_url, headers = headers)
# # e = etree.HTML(response.text)
# # text1 = e.xpath('//main[@id="c-718905313"]/p[1]/span[@class="content-text"]/text()')
# text1 = re.findall('\u003cp>　　(.*)\u003cp>', response.text)[0]
# text1 = text1.replace('</p><p>　　', '\n')
# print(text1)