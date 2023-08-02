import requests
import threading
from queue import Queue
from urllib import parse
from urllib import request
import os

filename = 'D:/Crawler/wallpaper/王者壁纸/'
if not os.path.exists(filename):
    os.mkdir(filename)


headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.183',
    'Referer':'https://pvp.qq.com/web201605/wallpaper.shtml'
}

#获取每张壁纸的各个分辨率图片
def exact_url(data):
    img_url_list = []
    for i in range(1, 9):
        img_url = parse.unquote(data['sProdImgNo_{}'.format(i)]).replace('200', '0')
        img_url_list.append(img_url)
    return img_url_list

#生产者线程
class Producer(threading.Thread):
    def __init__(self, page_queue, img_url_queue):
        super().__init__()
        self.page_queue = page_queue
        self.img_url_queue = img_url_queue
    def run(self):
        while not self.page_queue.empty():
            page_url = self.page_queue.get()
            response = requests.get(page_url, headers = headers)
            json_data = response.json()
            d = {}
            data_list = json_data['List']
            for data in data_list:
                img_url_list = exact_url(data)
                img_name = parse.unquote(data['sProdName'])
                d[img_name] = img_url_list
                for name in d:
                    dirpath = os.path.join(filename, name.strip(' ').replace('1:1', ' '))#拼接路径
                    if not os.path.exists(dirpath):
                        os.mkdir(dirpath)
                    #下载并保存
                    for index, img_url in enumerate(d[name]):
                        #生产图片的url
                        self.img_url_queue.put({'img_path': os.path.join(dirpath, f'{index + 1}.jpg'),'img_url': img_url})


#消费者线程
class Customer(threading.Thread):
    def __init__(self, img_url_queue):
        super().__init__()
        self.img_url_queue = img_url_queue
    def run(self):
        while True:
            try:
                img_obj = self.img_url_queue.get(timeout = 20)
                request.urlretrieve(img_obj['img_url'], img_obj['img_path'])
                print(f'{img_obj["img_path"]}下载完成')
            except:
                break

#定义一个启动线程函数
def start():
    page_queue = Queue(22)
    img_url_queue = Queue(1000)
    for i in range(0, 22):
        page_url = f'https://apps.game.qq.com/cgi-bin/ams/module/ishow/V1.0/query/workList_inc.cgi?activityId=2735&sVerifyCode=ABCD&sDataType=JSON&iListNum=20&totalpage=0&page={i}&iOrder=0&iSortNumClose=1&_everyRead=true&iTypeId=2&iFlowId=267733&iActId=2735&iModuleId=2735&_=1690709462096'
        # print(page_url)
        page_queue.put(page_url)

    #创建生产者线程对象
    for i in range(5):
        t = Producer(page_queue, img_url_queue)
        t.start()

    #创建消费者线程对象
    for i in range(10):
        t = Customer(img_url_queue)
        t.start()

if __name__ == '__main__':
    start()