import requests

headers = {
    "User_Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.82"
}
response = requests.get("https://movie.douban.com/top250", headers=headers)
print(response.status_code)

