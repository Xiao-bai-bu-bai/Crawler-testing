import pprint
import re
import time

import requests
from lxml import etree
from tqdm import tqdm

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Referer': 'https://www.huya.com/'
}
# 输入载荷

videoId = 757017261
data = {
    'videoId': videoId,
    'uid': '',
    '_': 1713345522975
}


def paly_video(url):
    response = requests.get(url, headers=headers, params=data)
    # 切换清晰度0,1,2分别是360p,720p,1080p
    info_json = response.json()['data']['moment']['videoInfo']['definitions'][2]['url']
    filename = response.json()['data']['moment']['title']
    return info_json, filename

def download_video(url, filename, path):
    response = requests.get(url, headers=headers)
    with open(f'{path}/{filename}.mp4', 'ab') as f:
        f.write(response.content)
    print(f'{filename}下载完成')

# 获取视频列表video_id
def get_video_list(index_url):
    response = requests.get(index_url, headers=headers)
    tree = etree.HTML(response.text)
    video_id_lists = tree.xpath('//ul[@class="vhy-video-list clearfix "]/li/@data-vid')
    return video_id_lists
    # for i in response.json()['data']['momentList']:
    #     print(i['videoId'])


if __name__ == '__main__':
    path = 'E:\python-learn\爬虫\简单练习\夜猫爬虫\虎牙视频\虎牙视频'
    index_url = 'https://www.huya.com/video/g/lolydzy'
    video_id_lists = get_video_list(index_url)
    url = 'https://liveapi.huya.com/moment/getMomentContent'
    for video_id in tqdm(video_id_lists):
        data['videoId'] = video_id
        info_json, filename = paly_video(url)
        download_video(info_json, filename, path)
        time.sleep(1)

