import scrapy


class BaiduSpider(scrapy.Spider):
    # 爬虫名
    name = "baidu"
    # 爬虫的域名：
    allowed_domains = ["www.baidu.com"]
    #起始url列表
    start_urls = ["https://www.baidu.com"]

    def parse(self, response):
        # 成员方法
        # 解析函数
        # urllib
        # request = urllib.request.Request(url...)
        # response = urllib.request.urlopen(request)
        # requests
        # response = requests.get(url)
        result = response.text
        print(response.status) #状态码
        print(response.headers)

        content = response.xpath("//input[@id='su']/@value")
        print(content)


