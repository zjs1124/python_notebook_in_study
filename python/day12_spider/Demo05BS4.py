"""
BS4基本概念

1、安装：pip install bs4
2、导包：from bs4 import BeautifulSoup
3、创建对象
    （1）本地文件生成对象
          soup = BeautifulSoup(open('1.html'), 'lxml')
    （2）服务器响应文件生成对象
      soup = BeautifulSoup(response.read().decode(), 'lxml')
4、基本语法
    （1）节点定位
        根据标签名查找节点。eg:soup.a
        获取标签的属性和属性值 eg:soup.a.attrs
    （2）函数
        find
        find_all
        select
"""

from bs4 import BeautifulSoup
# 通过解析本地文件，来讲bs4语法进行讲解
# UnicodeDecodeError: 'gbk' codec can't decode byte 0xad in position 302: illegal multibyte sequence
# 注意：默认打开文件的编码格式是gbk，所以在打开文件的时候要指定编码格式
soup = BeautifulSoup(open('bs4.html',encoding='utf-8'), 'lxml')
# print(soup)
# print(soup.a)   # <a class="a1" href="https://sc.chinaz.com/tupian/22121423693.htm" id="">科学家实验室科学研究图片</a>
# print(soup.a.attrs)

# ******************************节点的选择***********************************
# 1、find:查找节点并返回一个对象
# 返回的是第一个符合条件的数据
# print(soup.find('a'))

# 根据class的值来查找a标签
# print(soup.find('a',class_='a2'))  # <a class="a2" href="">兰智</a>



# 2、find_all:查找所有符合条件的节点，返回一个列表
# print(soup.find_all('a'))
# 如果想要获取多个标签的数据，在find_all函数的参数中添加列表的数据
# print(soup.find_all(['a','span']))

# 查找li标签的前两个数据
# limit:查找前几个数据
# print(soup.find_all("li",limit=2))

# 3、select:根据选择器得到节点对象 ***
#返回的结果是一个列表，并返回多个数据
# print(soup.select('a'))  # [<a class="a1" href="https://sc.chinaz.com/tupian/22121423693.htm" id="">科学家实验室科学研究图片</a>, <a class="a2" href="">兰智</a>]


# 查看a标签的class属性
# 类选择器     . 代表class
# bs4中 class 可以使用 . 来代替
# print(soup.select('.a1'))

# 查找id为d1的标签
# 类选择器     # 代表id
# bs4中 id 可以使用 # 来代替
# print(soup.select('#d1'))


# 属性选择器：通过属性来寻找对应的标签
# 查找li标签中id属性的标签
# print(soup.select('li[id]'))     # //li/@id

# 查找 li标签中id属性值为l2标签
# print(soup.select('li[id="l2"]'))



# 层级选择器
#     (1)后代选择器

# 查找div标签下面的li标签
# print(soup.select('div li'))   # //


#     (2)子代选择器
# 查找div标签下面的li标签
# print(soup.select('div > ul > li'))   # /

# 查找a标签和li标签的所有的对象
# print(soup.select('a,li'))




# *****************************节点的信息***********************************
# 获取节点内容，查找id属性为d1的标签
# result = soup.select('#d1')[0]
# print(result)
# print(type(result))


# print(result.get_text())
# print(result.string)  #None
# 注意：如果标签对象中，只有内容，那么string和get_text()都可以使用
# 如果标签对象中吗，除了内容还有标签，那么string就获取不到数据，返回None，而get_text()可以获取数据


# 节点数据
# obj = soup.select('#p1')[0]
# print(obj.name)   # p 获取的是标签的名称
# print(obj.attrs)  # 字典  # {'id': 'p1', 'class': ['p1']}


# 获取节点属性
obj = soup.select('#p1')[0]
print(obj)
print(obj.attrs.get("class"))  # ['p1']
print(obj.get("class"))  # 可以，但不推荐

print(obj["class"])