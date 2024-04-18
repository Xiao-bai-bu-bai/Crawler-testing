import pprint
import re
import time

import requests

cookies = {
    'kpf': 'PC_WEB',
    'clientid': '3',
    'did': 'web_6cd9f9be39c28ad16a2d286d2571d732',
    'didv': '1713404299061',
    '_bl_uid': 'y0lzqvwh4v8kCzoRgi7R0eeejpm2',
    'kpn': 'KUAISHOU_VISION',
}

headers = {
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    # 'Cookie': 'kpf=PC_WEB; clientid=3; did=web_6cd9f9be39c28ad16a2d286d2571d732; didv=1713404299061; _bl_uid=y0lzqvwh4v8kCzoRgi7R0eeejpm2; kpn=KUAISHOU_VISION',
    'Origin': 'https://www.kuaishou.com',
    'Referer': 'https://www.kuaishou.com/search/video?searchKey=%E4%BA%91%E9%A1%B6%E4%B9%8B%E5%A5%95',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
    'accept': '*/*',
    'content-type': 'application/json',
    'dnt': '1',
    'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

keyword = input('输入视频名称：')
json_data = {
    'operationName': 'visionSearchPhoto',
    'variables': {
        'keyword': keyword,
        'pcursor': '',
        'page': 'search',
    },
    'query': 'fragment photoContent on PhotoEntity {\n  __typename\n  id\n  duration\n  caption\n  originCaption\n  likeCount\n  viewCount\n  commentCount\n  realLikeCount\n  coverUrl\n  photoUrl\n  photoH265Url\n  manifest\n  manifestH265\n  videoResource\n  coverUrls {\n    url\n    __typename\n  }\n  timestamp\n  expTag\n  animatedCoverUrl\n  distance\n  videoRatio\n  liked\n  stereoType\n  profileUserTopPhoto\n  musicBlocked\n  riskTagContent\n  riskTagUrl\n}\n\nfragment recoPhotoFragment on recoPhotoEntity {\n  __typename\n  id\n  duration\n  caption\n  originCaption\n  likeCount\n  viewCount\n  commentCount\n  realLikeCount\n  coverUrl\n  photoUrl\n  photoH265Url\n  manifest\n  manifestH265\n  videoResource\n  coverUrls {\n    url\n    __typename\n  }\n  timestamp\n  expTag\n  animatedCoverUrl\n  distance\n  videoRatio\n  liked\n  stereoType\n  profileUserTopPhoto\n  musicBlocked\n  riskTagContent\n  riskTagUrl\n}\n\nfragment feedContent on Feed {\n  type\n  author {\n    id\n    name\n    headerUrl\n    following\n    headerUrls {\n      url\n      __typename\n    }\n    __typename\n  }\n  photo {\n    ...photoContent\n    ...recoPhotoFragment\n    __typename\n  }\n  canAddComment\n  llsid\n  status\n  currentPcursor\n  tags {\n    type\n    name\n    __typename\n  }\n  __typename\n}\n\nquery visionSearchPhoto($keyword: String, $pcursor: String, $searchSessionId: String, $page: String, $webPageArea: String) {\n  visionSearchPhoto(keyword: $keyword, pcursor: $pcursor, searchSessionId: $searchSessionId, page: $page, webPageArea: $webPageArea) {\n    result\n    llsid\n    webPageArea\n    feeds {\n      ...feedContent\n      __typename\n    }\n    searchSessionId\n    pcursor\n    aladdinBanner {\n      imgUrl\n      link\n      __typename\n    }\n    __typename\n  }\n}\n',
}

def get_video_url(url):
    response = requests.post(url, cookies=cookies, headers=headers, json=json_data)
    # 提取视频列表
    info = response.json()['data']['visionSearchPhoto']['feeds']
    # 提取视频地址
    play_urls = [i['photo']['videoResource']['h264']['adaptationSet'][0]['representation'][0]['url'] for i in info]
    filename = [i['photo']['caption'] for i in info]
    return play_urls, filename


def download_video(url, filename, path):
    if 'm3u8' in url:
        response = requests.get(url, headers=headers)
        file_ts = re.sub('#.*', '', response.text).split()
        first_ts = url.split('/')[:-1]
        first_ts = '/'.join(first_ts)
        with open(f'{path}/{filename}.mp4', 'ab') as f:
            for ts in file_ts:
                ts = first_ts + '/' + ts
                ts_content = requests.get(url=ts, headers=headers).content
                f.write(ts_content)
            print(f'{filename}下载完成')
    else:
        pass
        response = requests.get(url, headers=headers)
        with open(f'{path}/{filename}.mp4', 'ab') as f:
            f.write(response.content)
            print(f'{filename}下载完成')


if __name__ == '__main__':
    url = 'https://www.kuaishou.com/graphql'
    path = 'E:\python-learn\爬虫\简单练习\夜猫爬虫\快手视频\快手视频'

    play_urls, filename = get_video_url(url)
    for play_url, filename in zip(play_urls, filename):
        filename = re.sub(r'[#\/:*?"<>|\n<>]', '', filename)
        download_video(play_url, filename, path)
        time.sleep(0.5)