"""
get请求

"""
import requests

url = "https://www.baidu.com/s?"
data = {
    "wd":"刘德华"
}
headers = {
    "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36"
}
"""
url：请求资源路径
params：参数列表
**kwargs  字典
"""
response = requests.get(url=url,params=data,headers=headers)
# 获取网页源代码
content = response.text
print(content)


"""
总结：
1、参数使用params传递
2、参数无序urlencode编码
3、不需要请求对象定制
4、请求资源路径中的?可加可不加
"""