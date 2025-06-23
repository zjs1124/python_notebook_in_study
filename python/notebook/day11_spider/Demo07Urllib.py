"""
抓取豆瓣电影10页json数据
"""


# https://movie.douban.com/j/chart/top_list?type=13&interval_id=100%3A90&action=&start=0&limit=20
# https://movie.douban.com/j/chart/top_list?type=13&interval_id=100%3A90&action=&start=20&limit=20
# https://movie.douban.com/j/chart/top_list?type=13&interval_id=100%3A90&action=&start=40&limit=20
# https://movie.douban.com/j/chart/top_list?type=13&interval_id=100%3A90&action=&start=60&limit=20
# https://movie.douban.com/j/chart/top_list?type=13&interval_id=100%3A90&action=&start=80&limit=20




# page   1  2    3    4
# start  0  20   40   60
# start (page - 1) * 20

import urllib.request
import urllib.parse


# 发送请求
def create_request(page):
    base_url = "https://movie.douban.com/j/chart/top_list?type=13&interval_id=100%3A90&action=&"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    data = {
        "start":(page -1) * 20,
        "limit":20
    }
    data = urllib.parse.urlencode(data)
    url = base_url + data
    request = urllib.request.Request(url=url, headers=headers)
    return request

# 获取数据
def get_content(request):
    response = urllib.request.urlopen(request)
    content = response.read().decode("utf-8")
    return content



# 下载数据
#douban1.json
#douban2.json
#douban3.json
#douban4.json

def down_load(page,content):
    with open("douban" + str(page) + ".json", "w", encoding="utf-8") as f:
        f.write(content)


# 主程序

if __name__ == '__main__':
    # 开始
    start_page = int(input("请输入起始页码:"))
    # 结束
    end_page = int(input("请输入结束页码:"))

    # 使用for循环抓取10页内容
    for page in range(start_page,end_page + 1):
        # 发送请求(请求头定制)
        request = create_request(page)
        # 获取响应
        content = get_content(request)
        # 下载
        down_load(page,content)