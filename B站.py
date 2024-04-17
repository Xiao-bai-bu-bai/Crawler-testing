import json
import os
import pprint
import re

import requests
from lxml import etree

# 爬取视频页源代码
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Referer': 'https://www.bilibili.com/'  # 防盗链
}


def get_play_info(url):
    response = requests.get(url, headers=headers)
    info = re.findall('window.__playinfo__=(.+?)</script>', response.text, re.S)[0].strip()
    video_url = json.loads(info)['data']['dash']['video'][0]['baseUrl']
    audio_url = json.loads(info)['data']['dash']['audio'][0]['baseUrl']
    tree = etree.HTML(response.text)
    title = tree.xpath('//div[@class="video-info-title-inner"]/h1/text()')[0]
    return video_url, audio_url, title


# 提取视频和音频的url
def download_files(video_url, audio_url, title, path):
    video_content = requests.get(video_url, headers=headers).content
    audio_content = requests.get(audio_url, headers=headers).content

    with open(f'{path}/{title}.mp4', 'wb') as f:
        f.write(video_content)
        print(f'已下载{title}.mp4')
    with open(f'{path}/{title}.mp3', 'wb') as f:
        f.write(audio_content)
        print(f'已下载{title}.mp3')


# 下载并保存视频和音频
def merge_video_audio(title, path):
    cmd = fr'E:\爬虫\工具\ffmpeg\ffmpeg-4.4.1-essentials_build\ffmpeg-4.4.1-essentials_build\bin\ffmpeg -i {path}/{title}.mp4 -i {path}/{title}.mp3 -c:v copy -c:a aac -strict experimental {path}/output-{title}.mp4 -loglevel quiet'  # -loglevel quiet 清除输出日志
    os.system(cmd)
    print(f'{title}.mp4已合并')
    os.remove(f'{path}/{title}.mp4')
    os.remove(f'{path}/{title}.mp3')
    print(f'{title}.mp4和{title}.mp3已删除')


# 合并视频和音频


if __name__ == '__main__':
    url = 'https://www.bilibili.com/video/BV1pq421A7Tm/?spm_id_from=333.1007.tianma.1-1-1.click&vd_source=3e9b2185f8745ab7e959a312adeaa199'
    path = 'E:\python-learn\爬虫\简单练习\夜猫爬虫\B站视频\B站视频'
    video_url, audio_url, title = get_play_info(url)
    download_files(video_url, audio_url, title, path)
    merge_video_audio(title, path)
