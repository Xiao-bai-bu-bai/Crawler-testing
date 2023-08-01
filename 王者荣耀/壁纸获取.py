import requests
import os
from urllib import parse
from urllib import request
#解析url
# result = parse.unquote('https%3A%2F%2Fshp%2Eqpic%2Ecn%2Fishow%2F2735042818%2F1682676155%5F1265602313%5F14889%5FsProdImgNo%5F8%2Ejpg%2F200')
# print(result)

filename = 'D:/wallpaper/王者壁纸/'
if not os.path.exists(filename):
    os.mkdir(filename)

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.183',
    'Referer':'https://pvp.qq.com/'
}

#获取json数据
def send_request():
    url = 'https://apps.game.qq.com/cgi-bin/ams/module/ishow/V1.0/query/workList_inc.cgi?activityId=2735&sVerifyCode=ABCD&sDataType=JSON&iListNum=20&totalpage=0&page=0&iOrder=0&iSortNumClose=1&_everyRead=true&iTypeId=2&iFlowId=267733&iActId=2735&iModuleId=2735&_=1690709462096'
    response = requests.get(url, headers=headers)
    return response.json()

#获取每张壁纸的各个分辨率图片
def exact_url(data):
    img_url_list = []
    for i in range(1, 9):
        img_url = parse.unquote(data['sProdImgNo_{}'.format(i)]).replace('200', '0')
        img_url_list.append(img_url)
    return img_url_list

#通过上面两个方法获取一个字典包含图片名称和下载链接
def parse_json(json_data):
    d = {}
    data_list = json_data['List']
    for data in data_list:
        img_url_list = exact_url(data)
        img_name = parse.unquote(data['sProdName'])
        d[img_name] = img_url_list
        '''for item in d:
            print(item, d[item])'''
    save_jpg(d)

#保存每张图片相同的壁纸放在一个文件夹下面
def save_jpg(d):
    for name in d:
        dirpath = os.path.join(filename, name.strip(' '))
        os.mkdir(dirpath)
        for index, img_url in enumerate(d[name]):
            request.urlretrieve(img_url, os.path.join(dirpath,'{}.jpg').format(index+1))
            print('{}下载完毕'.format(d[name][index]))

#串联方法
def star():
    json_data = send_request()
    parse_json(json_data)


if __name__ == '__main__':
    star()

