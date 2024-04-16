import os.path
import pprint
import time

import requests
import re
import json

from lxml import etree
from tqdm import tqdm

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',

}


# 获取m3u8文件
def get_m3u8_url(url):
    response = requests.get(url, headers=headers)
    info = re.findall('window.pageInfo = window.videoInfo = (.+?)window.videoResource = {}', response.text, re.S)[
               0].strip()[:-1]
    info_json = json.loads(json.loads(info)['currentVideoInfo']['ksPlayJson'])['adaptationSet'][0]['representation'][0][
        'url']
    filename = json.loads(info)['title']
    # pprint.pprint(info_json)
    # print(filename)
    return info_json, filename


# 提取m3u8文件中的ts文件
def m3u8_ts(url):
    response = requests.get(url, headers=headers)
    ts_files = re.sub('#.*', '', response.text).split()
    # print(ts_files)
    return ts_files


# 下载并合并ts文件
def download_merge_ts(ts_files, filename, path):
    with open(f'{path}/{filename}.mp4', 'ab') as f:
        for ts in tqdm(ts_files):
            ts = 'https://tx-safety-video.acfun.cn/mediacloud/acfun/acfun_video/' + ts
            ts_content = requests.get(url=ts, headers=headers).content
            f.write(ts_content)


# 获取目录下所有文件
def get_all_files(index_url):
    response = requests.get(index_url, headers=headers)
    tree = etree.HTML(response.text)
    a_lists = tree.xpath('//div[@class="list-wrapper"]/div/a[@class="list-content-top"]/@href')
    a_lists = ['https://www.acfun.cn' + i for i in a_lists]
    print(a_lists)
    return a_lists



def main():
    index_url = 'https://www.acfun.cn/v/list136/index.htm'
    path = 'E:\python-learn\爬虫\简单练习\夜猫爬虫\A站视频\A站视频'
    a_lists = get_all_files(index_url)
    for url in a_lists:
        m3u8_url, filename = get_m3u8_url(url)
        ts_files = m3u8_ts(m3u8_url)
        download_merge_ts(ts_files, filename, path)
        time.sleep(1)



if __name__ == '__main__':
    main()
