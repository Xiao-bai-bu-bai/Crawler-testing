import os

import requests
from concurrent.futures import ThreadPoolExecutor, wait

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',

}


def download_one_video(url, i, path):
    '''
    下载视频
    :param url:
    :return:
    '''
    print(url, i, '开始下载')
    resp = requests.get(url, headers=headers)
    with open(os.path.join(path, f'{i}.ts'), 'wb') as f:
        f.write(resp.content)
    print(url, i, '结束下载')


def download_all_videos(path):
    if not os.path.exists(path):
        os.mkdir(path)
    # 存储目录
    with open('first.m3u8', encoding="UTF-8") as f:
        data = f.readlines()

    # 创建线程池
    poole = ThreadPoolExecutor(50)
    tasks = []

    i = 0
    for line in data:
        if line.startswith('#'):
            continue
        # print(line.strip())
        ts_url = line.strip()
        tasks.append(poole.submit(download_one_video, ts_url, i, path))
        i += 1

    # 等待
    wait(tasks)


def merge(path, filename='output'):
    '''
    进行ts文件合并 解决视频音频不同步的问题 建议使用这种
    :param filePath:
    :return:
    '''
    os.chdir(path)  # 进入到当前的ts文件夹内
    cmd = f'ffmpeg -i first.m3u8 -c copy {filename}.mp4'
    os.system(cmd)


# 处理m3u8文件中的url问题
def do_m3u8_url(path, m3u8_filename="first.m3u8"):
    # 这里还没处理key的问题
    if not os.path.exists(path):
        os.mkdir(path)
    # else:
        # shutil.rmtree(path)
        # os.mkdir(path)
    with open(m3u8_filename, mode="r", encoding="utf-8") as f:
        data = f.readlines()
    fw = open(os.path.join(path, m3u8_filename), 'w', encoding="utf-8")
    abs_path = os.getcwd()
    i = 0
    for line in data:
        # 如果不是url 则走下次循环
        if line.startswith("#"):
            fw.write(line)
        else:
            fw.write(f'{abs_path}/{path}/{i}.ts\n')
            i += 1


if __name__ == '__main__':
    path = '../ts'
    # download_all_videos(path)
    # do_m3u8_url(path)
    merge(path, '琅琊榜')
