import requests

main_url = 'https://xueqiu.com/'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',

}
# 创建一个session对象
session = requests.session()
# 拿到响应的cookie
session.get(url=main_url, headers=headers)

url = 'https://xueqiu.com/statuses/hot/listV2.json?since_id=-1&max_id=606695&size=15'

# 自动携带了cookie
response = session.get(url, headers=headers)
print(response)
print(response.json())