import re
import requests
import json
url = 'https://api.live.bilibili.com/xlive/web-interface/v1/second/getList?platform=web&parent_area_id=2&area_id=102&sort_type=&page=1&vajra_business_key=&web_location=444.43&w_rid=5a8a3b662784b0572971bf2a0e0f1efd&wts=1747401706'

headers = {
    "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/53",
    "cookie":"DedeUserID=163181975; DedeUserID__ckMd5=2dabab4cd3810ead; enable_web_push=DISABLE; header_theme_version=CLOSE; fingerprint=20cab6e73f818d27c65994914a7b59a8; buvid_fp_plain=undefined; buvid_fp=c093acc40381a6248cc7f8f1a74894ba; buvid3=98F2745E-AD72-E455-822A-5C47975FCF6B75993infoc; b_nut=1730227475; _uuid=A1C33617-22AA-410DB-398A-B7C107698EE1B76212infoc; enable_feed_channel=ENABLE; rpdid=|(JRu)~l)kRR0J'u~Ru)~YJJk; buvid4=CE39BC15-64D8-3F42-17B2-48AB32AAC73856992-022031700-SLoeSgX5CuG%2FaA7talL72A%3D%3D; LIVE_BUVID=AUTO6417419465324583; Hm_lvt_8a6e55dbd2870f0f5bc9194cddf32a02=1741946537; hit-dyn-v2=1; SESSDATA=1a560b47%2C1762867309%2C15846%2A52CjAqEFXLe4QCkZdYaJEH2iMbDEKHvusnTwYyjiblV2VfPdT0oZz6pYrZJbGVhSPt558SVlVta0RvMHRtTF9DaDV2VEIwTTNqRmhFc2tVLS1yQnQzVC05X3dTSW1DbXF6d282emxIZDhraUZ1QWt6X1lweXdnVk9sT25mSzlBeGNDeWZJWW1oU3FRIIEC; bili_jct=8dcffa8f68e536e7394425d62385afa7; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NDc2NTcyNTcsImlhdCI6MTc0NzM5Nzk5NywicGx0IjotMX0.EE4fGCiPP0pl15JOm0cWJvwImU4YiPKZAhf_Qb6lQ3Q; bili_ticket_expires=1747657197; bp_t_offset_163181975=1067559222872375296; CURRENT_FNVAL=4048; b_lsid=647C11085_196D93E2E82; bsource=search_baidu; home_feed_column=4; browser_resolution=767-438; PVID=16",
    "referer":"https://live.bilibili.com/"
}

response = requests.get(url = url,headers = headers)
# data_list = response.json().get("data").get("list")
# print(data_list)
# resp_1 = requests.get(url, headers=header)
response.encoding = "utf-8"
html_data = response
data_list = re.findall(r"__INITIAL_STATE__=(.+);\(function", html_data.text)
data_drict = json.loads(data_list[0])
oid = data_drict["aid"]
print(oid)