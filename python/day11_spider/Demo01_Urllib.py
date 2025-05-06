"""
urllib.request
可以模拟浏览器的一个请求发起过程
浏览器发送请求的方法：Get、Post
# urllib.request 的 urlopen 方法来打开一个 URL
"""
# https://www.baidu.com/
import urllib.request

# 需要打开的url
url = "https://www.baidu.com/"
response = urllib.request.urlopen(url)
print(response)  # <http.client.HTTPResponse object at 0x0000019A9418FDC0>

# urllib.request 一个类型HTTPResponse、六个方法
# 1、read() 按照一个一个字节去读
# content = response.read()
# print(content)

# 思考？read(5)
# content = response.read(5)
# print(content)

# 2、readline() 读取一行内容
# content = response.readline()
# print(content)

# 3、readlines() 读取所有内容（一行一行的读取）
# content = response.readlines()
# print(content)

# 4、getcode()  获取状态码
# print(response.getcode())  # 200

# 200 成功
# 常见的状态码：
# 200
# 404
# 505
# 504

# 5、getUrl() 获取url
# print(response.geturl())   # https://www.baidu.com/


# 6、getheaders() 获取响应头
# print(response.getheaders())


# urllib.request.urlretrieve 下载
# img_url = "https://www.baidu.com/img/PCtm_d9c8750bed0b3c7d089fa7d55720d6cf.png"
# urllib.request.urlretrieve(img_url,"logo.png")

# # 下载网页
# html_url = "https://www.baidu.com/"
# urllib.request.urlretrieve(html_url,"baidu.html")

# 下载视频
# video_url = "https://video.pearvideo.com/mp4/short/20250411/cont-1799384-16049207-hd.mp4"
# urllib.request.urlretrieve(video_url, "video.mp4")
