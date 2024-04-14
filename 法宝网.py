import time

import requests
from lxml import etree

headers = {
    'Accept': '*/*',
    # 'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Content-Length': '856',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Cookie': 'x_vpn_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6IjNYQVkxRUNKIiwiZXhwIjoxNzEzMDgyMjEyLCJpc3MiOiJ3d3cueHh4LmNvbSIsImF1ZCI6Ind3dy54eHguY29tIn0.qkeD49PjnEt2i4Cg7Ox_CtSXnsgnYQCfyq-W6BiDgiI; refresh=0',
    'Dnt': '1',
    'Host': 'jjll.tytyxdy.com',
    'Origin': 'https://jjll.tytyxdy.com',
    'Referer': 'https://jjll.tytyxdy.com/https/44696469646131313237446964696461bd6feb2613c3be1bcd4ca96fd868/case?way=topGuid',
    'Sec-Ch-Ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': '"Windows"',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
}

data = {

    'Menu': 'case',
    'Keywords': '',
    'SearchKeywordType': 'Title',
    'MatchType': 'Exact',
    'RangeType': 'Piece',
    'Library': 'pfnl',
    'ClassFlag': 'pfnl',
    'GroupLibraries': '',
    'QueryOnClick': False,
    'AfterSearch': False,
    'PreviousLib': 'pfnl',
    'pdfStr': '',
    'pdfTitle': '',
    'IsSynonymSearch': False,
    'RequestFrom': '',
    'LastLibForChangeColumn': 'pfnl',
    'IsAdv': False,
    'ClassCodeKey': '%2C%2C%2C%2C%2C%2C%2C%2C%2C%2C%2C',
    'Aggs.CategoryIntegration': '',
    'Aggs.CaseGrade': '03',
    'Aggs.CaseClass': '',
    'Aggs.SubjectClassSpecialType': '',
    'Aggs.CourtGrade': '',
    'Aggs.LastInstanceCourt': '',
    'Aggs.TrialStep': '',
    'Aggs.DocumentAttr': '',
    'Aggs.LastInstanceDate': '',
    'Aggs.TrialStepCount': '',
    'Aggs.NoPublicReason': '',
    'Aggs.WordNum': '',
    'GroupByIndex': 0,
    'OrderByIndex': 0,
    'ShowType': 'Default',
    'GroupValue': '',
    'TitleKeywords': '',
    'FullTextKeywords': '',
    'Pager.PageIndex': 0,
    'RecordShowType': 'List',
    'Pager.PageIndex': 0,
    'Pager.PageSize': 100,
    'QueryBase64Request': '',
    'VerifyCodeResult': '',
    'isEng': 'chinese',
    'OldPageIndex': '',
    'newPageIndex': '',
    'IsShowListSummary': '',
    'X-Requested-With': 'XMLHttpRequest',
}


def get_content(url):
    # session = requests.session()
    # session.get('https://jjll.tytyxdy.com/', headers=headers)

    response = requests.get(url, headers=headers)
    tree = etree.HTML(response.text)

    strongs_text = tree.xpath('//div[@class="box"]//text()')
    strongs_text = [i.strip() for i in strongs_text]
    strongs_text = [
        i.replace('案由：', '\n案由：').replace('案 号：', '\n案 号：').replace('案由：', '\n案由：').replace('文书类型：',
                                                                                                        '\n文书类型：').replace(
            '公开类型：', '\n公开类型：').replace('审结日期：', '\n审结日期：').replace('审理法院：', '\n审理法院：').replace(
            '案件类型：', '\n案件类型：').replace('审理程序：', '\n审理程序：').replace('案例发文：', '\n案例发文：').replace(
            '发布主题：', '\n发布主题：').replace('案例编号：', '\n案例编号：').replace('发布日期：', '\n发布日期：').replace(
            '该指导性案例被应用情况：', '\n该指导性案例被应用情况：') for i in strongs_text if i != '']
    strongs_text = ''.join(strongs_text[37:-32])
    content = tree.xpath('//div[@class="fulltext"]//text()')
    content = [i.strip() for i in content]
    content = [i.replace('getty\n                    Images', 'getty Images').replace('\n                        ',
                                                                                      '').replace('【', '\n【').replace(
        '】', '】\n') for i in content if i != '']
    content = ''.join(content)
    return strongs_text, content


def get_title_url(index_url):
    response = requests.post(index_url, data=data, headers=headers)
    tree = etree.HTML(response.text)

    # 标题链接
    title_as = tree.xpath('//div[@class="t"]/h4/a/@href')
    titles = tree.xpath('//div[@class="t"]/h4/a/text()')

    title_as = ['https://jjll.tytyxdy.com/https/44696469646131313237446964696461bd6feb2613c3be1bcd4ca96fd868' + i for i in title_as if i != '']
    titles = [i for i in titles if i != '']
    return title_as, titles


def download_content(title_as, titles, path):
    for title, title_a in zip(titles, title_as):
        strongs_text, content = get_content(title_a)
        with open(f'{path}/{title}.txt', 'a', encoding='utf-8') as f:
            f.write(title + '\n\n' + strongs_text + '\n\n' + content + '\n\n')
        print(f'{title}下载完成')
        time.sleep(1)


if __name__ == '__main__':
    index_url = 'https://jjll.tytyxdy.com/https/44696469646131313237446964696461bd6feb2613c3be1bcd4ca96fd868/case/search/RecordSearch?vpn-12-o2-www.pkulaw.com'
    path = 'E:\python-learn\爬虫\简单练习\某大法宝网\数据'
    title_as, titles = get_title_url(index_url)

    download_content(title_as, titles, path)
    print('全部下载完成')

'''
https://jjll.tytyxdy.com/pfnl/08df102e7c10f206a4dc8cb3c9afd6bbf6fab895cef22475bdfb.html?way=listView

https://jjll.tytyxdy.com/https/44696469646131313237446964696461bd6feb2613c3be1bcd4ca96fd868/pfnl/08df102e7c10f206a4dc8cb3c9afd6bbf6fab895cef22475bdfb.html?way=listView

'''