import requests
from lxml import etree

html_url = 'https://www.zongheng.com/rank/details.html?rt=1&d=1&i=2'

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.183'
}
response = requests.get(html_url, headers = headers)
# print(response.text)

e = etree.HTML(response.text)
names = e.xpath('//div[@class="rankpage_box"]/div[@class="rank_d_list borderB_c_dsh clearfix"]/div[2]/div[@class="rank_d_b_name"]/a/text()')
lists = e.xpath('//div[@class="rankpage_box"]/div[@class="rank_d_list borderB_c_dsh clearfix"]/div[2]/div[@class="rank_d_b_cate"]/a/text()')
authors = [i for i in lists[::3]]
kinds = [i for i in lists[1::3]]
statuses = [i for i in lists[2::3]]

# for name, auther, kinds, statues in zip(names, authors, kinds, statuses):
#     print(f'{name}---{auther}---{kinds}---{statues}')