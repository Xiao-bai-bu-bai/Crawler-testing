import time
from random import uniform

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

service = Service(executable_path='C:\Program Files\Google\Chrome\Application\chromedriver.exe')
opt = webdriver.ChromeOptions()

opt.add_argument('--disable-blink-features=AutomationControlled')
opt.add_experimental_option('excludeSwitches', ['enable-automation'])

browser = webdriver.Chrome(options=opt)
browser.maximize_window()
browser.implicitly_wait(5)
browser.get('https://www.tiktok.com/@redbullbe/video/7389649260330880289')
time.sleep(uniform(2, 4))
title = browser.find_element(By.XPATH, '(//h1[@data-e2e="browse-video-desc"]/span)[1]').text
# 点赞数、评论数、收藏数、分享数
like = browser.find_element(By.XPATH, '(//strong[@class="css-n6wn07-StrongText edu4zum2"])[1]').text
comment = browser.find_element(By.XPATH, '(//strong[@class="css-n6wn07-StrongText edu4zum2"])[2]').text
collect = browser.find_element(By.XPATH, '(//strong[@class="css-n6wn07-StrongText edu4zum2"])[3]').text
share = browser.find_element(By.XPATH, '(//strong[@class="css-n6wn07-StrongText edu4zum2"])[4]').text
print(f"视频标题: {title}, 点赞数: {like}, 评论数: {comment}, 收藏数: {collect}, 分享数: {share}")

# 滚动到特定div的底部加载更多内容
target_div_xpath = '//div[@class="css-13revos-DivCommentListContainer ekjxngi3"]'  # 替换为实际的div的XPath
last_height = browser.execute_script(
    f"return document.evaluate('{target_div_xpath}', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.scrollHeight")

while True:
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(uniform(1, 2))  # 等待内容加载
    new_height = browser.execute_script(
        f"return document.evaluate('{target_div_xpath}', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.scrollHeight")
    if new_height == last_height:
        print("已滚动到底部，没有更多内容")
        break
    last_height = new_height

with open('tiktok.csv', mode='a', encoding='utf-8') as f:
    f.write(f"{title},{like},{comment},{collect},{share}\n")
    comment_collapses = browser.find_elements(By.XPATH, "//p[contains(@data-e2e, 'view-more-')]")

    while comment_collapses:
        try:
            cc = comment_collapses[0]
            # 滚动页面使元素可见
            browser.execute_script(
                "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center', inline: 'center'});",
                cc)
            time.sleep(1.5)

            # 使用 ActionChains 执行点击操作
            ActionChains(browser).move_to_element(cc).click().release().perform()
            comment_collapses = browser.find_elements(By.XPATH, "//p[contains(@data-e2e, 'view-more-')]")

        except Exception as e:
            print(f"点击按钮时出错: {e}")
            continue

    # 获取所有评论
    # comment_first = browser.find_elements(By.XPATH, '//p[@data-e2e="comment-level-1"]')
    # comment_second = browser.find_elements(By.XPATH, '//p[@data-e2e="comment-level-2"]')
    comment_list = browser.find_elements(By.XPATH, '//div[@class="css-1i7ohvi-DivCommentItemContainer eo72wou0"]')
    for comment in comment_list:

        # 尝试查找 comment-level-1 元素
        comment_first_list = comment.find_elements(By.XPATH, './/p[@data-e2e="comment-level-1"]')
        for comment_first in comment_first_list:
            f.write(f"{comment_first.text.strip()}\n")
            print(1)
        # 尝试查找 comment-level-2 元素
        try:
            comment_second_list = comment.find_elements(By.XPATH, './/p[@data-e2e="comment-level-2"]')
            if comment_second_list:
                for comment_second in comment_second_list:
                    f.write(f"\t{comment_second.text.strip()}\n")
                    print(2)
        except Exception:
            print("没有第二级评论")
    print("评论已保存")
