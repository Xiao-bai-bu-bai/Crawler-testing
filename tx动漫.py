import os
import time

import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

service = Service(executable_path='C:\Program Files\Google\Chrome\Application\chromedriver.exe')
opt = Options()
opt.add_argument('--disable-blink-features=AutomationControlled')


# opt.add_argument('--headless')


def download(url, path):
    browser = webdriver.Chrome(options=opt, service=service)
    browser.maximize_window()  # 最大化浏览器
    browser.get(url)
    time.sleep(1)

    pic_list = browser.find_elements(By.XPATH, '//div[@class="main"]/ul/li/img')
    filename = browser.find_element(By.XPATH, '//*[@class="title"]/span[@class="title-comicHeading"]').text
    print(filename)

    for num, pic in enumerate(pic_list):
        time.sleep(0.5)
        # 滚动到指定元素加载数据
        ActionChains(browser).scroll_to_element(pic).perform()
        # 获取属性元素
        link = pic.get_attribute('src')
        pic_content = requests.get(link).content
        if not os.path.exists(f'{path}/{filename}'):
            os.mkdir(f'{path}/{filename}')
        with open(f'{path}/{filename}/{num}.jpg', 'wb') as f:
            f.write(pic_content)
            print(f"第{num}张下载完成")
    next_url = browser.find_element(By.XPATH, '//*[@id="mainControlNext"]').get_attribute('href')

    browser.close()
    return next_url


if __name__ == '__main__':
    path = 'E:\python-learn\爬虫\简单练习\夜猫爬虫\\tx动漫'
    url = 'https://ac.qq.com/ComicView/index/id/531040/cid/1'
    while url:
        url = download(url, path)
