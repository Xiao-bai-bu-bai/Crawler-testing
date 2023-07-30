import requests
from lxml import etree
import os
#文件保存路径
filename = 'D:/wallpaper//'
if not os.path.exists(filename):
    os.mkdir(filename)
#全部英雄路径
html_url = 'https://pvp.qq.com/web201605/js/herolist.json'

#一如既往地伪装
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.183'
}

#获取保存全部英雄的json文件
response = requests.get(html_url, headers = headers).json()
# print(response)
num = [i.get('ename') for i in response]#英雄编号
name = [i.get('cname') for i in response]#英雄名称
# print(num, name)

name1 = input('请输入要下载的英雄名称：')
if name1 in name:#判断是否为王者英雄
    name_index = name.index(name1)#获取想要下载英雄的下标
    # print(num[name_index])

    list_url = f'https://pvp.qq.com/web201605/herodetail/{num[name_index]}.shtml'#通过下标找英雄编号，都是一一对应的
    response1 = requests.get(list_url, headers = headers)#获取英雄界面
    response1.encoding = 'gbk'#改变编码格式为gbk否则出现乱码
    e = etree.HTML(response1.text)

    picture_name = e.xpath('//div[@class="pic-pf"]/ul/@data-imgname')[0]#查找皮肤名称
    picture_name = [i[:i.index('&')]for i in picture_name.split('|')]#分割名称
    for name in picture_name:
        picture_url = f'https://game.gtimg.cn/images/yxzj/img201606/skin/hero-info/{num[name_index]}/{num[name_index]}-bigskin-{picture_name.index(name) + 1}.jpg'#通过下标填入英雄编号以及皮肤编号
        picture_content = requests.get(picture_url, headers=headers).content#获取二进制数据
        with open(filename + name + '.jpg', mode='ab') as f:#以二进制追加写入
            f.write(picture_content)
        print(f'{name}保存成功，就在D盘的wallpaper文件下面')
else:
    print('输入错误， 我看你小子没玩过王者吧')





#

