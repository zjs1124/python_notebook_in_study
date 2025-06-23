"""
cookie登录

"""
import urllib.request
import json
# https://m.weibo.cn/profile/6421136270
# url = "https://m.weibo.cn/u/6421136270"
# url = "https://m.weibo.cn/api/container/getIndex?type=uid&value=6421136270&containerid=1005056421136270"

url = "https://m.weibo.cn/users/6421136270?set=1"
headers = {
    "accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
    "cookie":"_T_WM=72889762665; SCF=AnfdacrRgvQqEnX06MAhvQHaEv4NfxnFsPrcv1-oPQx2xT--jdXY77rqm8w41GMrUR_SBTMskmuCKLpIRE8xI5E.; SUB=_2A25FGDu2DeRhGeBK6VMQ8yjOzDyIHXVmVDF-rDV6PUJbktAbLUelkW1NR_SGujo3CDm3cX6bZnn4uP_4SiHukMFn; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5hZ4JqvRTngq9Tma-_2Ggu5NHD95QcShzpeKeceoM7Ws4Dqc_Zi--fi-isi-8Fi--Xi-z4iK.7i--ciK.RiKLsi--NiK.7iKn0i--fiKLhi-2Ri--4iKn7iKn0i--fi-zpiKnfi--ci-z7iK.pBXet; SSOLoginState=1746684903; ALF=1749276903; MLOGIN=1; M_WEIBOCN_PARAMS=luicode%3D10000011%26lfid%3D1076036421136270; XSRF-TOKEN=685c54; mweibo_short_token=6d7bc9d118"
    # 添加其他信息
}

# 请求头定制
request = urllib.request.Request(url=url,headers=headers)

# 模拟浏览器向服务器发送请求
response = urllib.request.urlopen(request)


# 获取响应的数据
content = response.read().decode("utf-8")
print(content)


# 将数据保存为html
with open("cookie.html","w",encoding="utf-8") as fp:
    fp.write(content)



