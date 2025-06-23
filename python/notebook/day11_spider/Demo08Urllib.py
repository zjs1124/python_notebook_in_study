"""
ajax的post请求
"""
"""
https://www.kfc.com.cn/kfccda/ashx/GetStoreList.ashx?op=cname

cname: 合肥
pid: 
pageIndex: 3
pageSize: 10
"""
import urllib.request
import urllib.parse
# 请求头定制
def create_request(page):
    base_url = "https://www.kfc.com.cn/kfccda/ashx/GetStoreList.ashx?op=cname"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    }

    data = {
        "cname": "合肥",
        "pid": "",
        "pageIndex": page,
        "pageSize": 10
    }

    data = urllib.parse.urlencode(data).encode("utf-8")
    request = urllib.request.Request(url=base_url, data=data, headers=headers)
    return request




# 获取数据
def get_content(request):
    response = urllib.request.urlopen(request)
    content = response.read().decode("utf-8")
    return content


# 下载数据
def down_load(page,content):
    with open("kfc" + str(page) + ".json","w",encoding="utf-8") as file:
        file.write(content)


# 主程序
if __name__ == '__main__':
    start_page = int(input("请输入起始页码:"))
    end_page = int(input("请输入结束页码:"))
    for page in range(start_page,end_page + 1):
        # 请求头定制
        request = create_request(page)
        # 获取数据
        content = get_content(request)
        # 下载数据
        down_load(page,content)


