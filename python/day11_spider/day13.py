import urllib.request
url = 'https://www.baidu.com/'
response = urllib.request.urlopen(url)
# 1.read() 读取一个一个字节
# content = response.read(5)
# print(content)
# print(content)
# 2.readline()读取一行
# content = response.readline()
# print(content)
# 3.readlines() 读取所有行
# content = response.readlines()
# print(content)
# 4，getcode()获取状态码
# print(response.getcode())
'''
状态码
200 成功获取
404 notfound
505 http version not supported
504 gateway time-out 充当网关或者代理的服务器，未及时获取远端服务器的请求

'''
# 5.geturl()获取url
# print(response.geturl())https://www.baidu.com/

#6. getheaders() 获取响应头
# print(response.getheaders())

# 7.下载
#urllib.request.urlretrieve
# img_url = "https://www.baidu.com/img/PCtm_d9c8750bed0b3c7d089fa7d55720d6cf.png"
# urllib.request.urlretrieve(img_url,'logo1.png')

"""
url的组成
https://www.baidu.com/s?&wd=python
1.协议:http/https
2.主机:www.baidu.com
3.端口号 http:80 https:443
4.路径:s
5.参数:wd=python
6.锚点:#
"""
# import urllib.request
# url = "https://www.baidu.com/"
# response = urllib.request.urlopen(url)
# html = response.read().decode('utf-8') decode解码,encode编码
# print(html)

