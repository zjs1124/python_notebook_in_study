"""
使用Xpath解析
1、本地文件
2、服务器响应文件（重点）
"""
from lxml import etree


# 解析本地文件
html_etree = etree.parse("hello.html")
# print(html_etree)  # <lxml.etree._ElementTree object at 0x0000026F314A0B40>


# 1、查找ul下面的li标签
# li_list  = html_etree.xpath("/html/body/ul/li")
# li_list  = html_etree.xpath("//ul/li")
# li_list  = html_etree.xpath("//li/..")
# li_list  = html_etree.xpath("//li/.")



# 2、查找所有id属性的li标签
# li_list = html_etree.xpath('//ul/li[@id]')
# li_list = html_etree.xpath('//ul/li[@id]/text()')  # ['蜀山区', '包河区', '庐阳区']


# 3、查找id为l1的li标签

# li_list = html_etree.xpath('//ul/li[@id="l1"]/text()')
# print(li_list)
# print(li_list[0])

# 4、查找id为l1标签的class属性值
# li_list = html_etree.xpath('//ul/li[@id="l1"]/@class')
# print(li_list)


# 5、查找id中包含l的li标签
# li_list = html_etree.xpath('//ul/li[contains(@id,"lz")]/text()')
# print(li_list)


# 6、查找id的值以l开头的li标签
# li_list = html_etree.xpath('//ul/li[starts-with(@id,"l")]/text()')
# print(li_list)


# 7、查找id为 l6 和 l7的li标签
# li_list  = html_etree.xpath('//ul/li[@id="l6"] or li[@id="l7"]')   # 错误示范
# li_list  = html_etree.xpath('//ul/li[@id="l5" and @class="c5"]/text()')
# print(li_list)


# 8、查找第三li标签
li_list = html_etree.xpath('//ul/li[position() < 4]/text()')
print(li_list)
