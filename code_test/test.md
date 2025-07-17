引入
思考两个问题？
第一个问题：数据如何存储？
第二个问题：数据如何处理？

Python数据处理
#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：python-learn 
@File    ：gen_data.py
@IDE     ：PyCharm 
@Author  ：JWchen
@Date    ：2025/2/22 14:11 
'''

"""
使用python代码生成卡口过车数据，生成将数据保存到txt文件中
数据字段列表
1、车牌号
2、卡口编号
3、卡口所在城市
4、车辆品牌
5、道路编号
6、车辆速度
7、车辆行驶方向
8、车辆通过时间
"""
import random
import string
from datetime import datetime


# 生成随机车牌号
def generate_plate_number():
    # 车牌号格式：省份简称 + 字母 + 5位数字/字母
    provinces = ["京"]
    letters = string.ascii_uppercase
    numbers = ''.join(random.choices(string.digits, k=5))
    return random.choice(provinces) + random.choice(letters) + numbers


# 生成随机卡口编号
def generate_gateway_id():
    return 'G' + ''.join(random.choices(string.digits, k=4))


# 生成随机城市
def generate_city():
    cities = ["北京", "上海", "广州", "深圳", "杭州", "成都", "武汉", "南京", "重庆", "天津"]
    return random.choice(cities)


# 生成随机车辆品牌
def generate_car_brand():
    brands = ["丰田", "大众", "本田", "宝马", "奔驰", "奥迪", "比亚迪", "特斯拉", "现代", "福特"]
    return random.choice(brands)


# 生成随机道路编号
def generate_road_id():
    return 'R' + ''.join(random.choices(string.digits, k=3))


# 生成随机车辆速度
def generate_speed():
    return random.randint(20, 120)  # 速度范围：20-120 km/h


# 生成随机车辆行驶方向
def generate_travel_direction():
    directions = ["上行", "下行"]
    return random.choice(directions)


# 生成一条卡口过车记录
def generate_record():
    plate_number = generate_plate_number()
    gateway_id = generate_gateway_id()
    city = generate_city()
    car_brand = generate_car_brand()
    road_id = generate_road_id()
    speed = generate_speed()
    travel_direction = generate_travel_direction()

    return f"{plate_number},{gateway_id},{city},{car_brand},{road_id},{speed},{travel_direction}"


# 生成多条记录并保存到txt文件
def generate_and_save_records(file_path, num_records):
    with open(file_path, 'w', encoding='utf-8') as file:
        for _ in range(num_records):
            record = generate_record()
            file.write(record + "\n")


# 主函数
if __name__ == "__main__":
    file_path = "D:\\pythoncode\\bigdata35\\data\\gateway_records2.txt"  # 保存文件的路径
    num_records = 10000000  # 生成10000000条记录
    generate_and_save_records(file_path, num_records)
    print(f"已生成 {num_records} 条卡口过车数据并保存到 {file_path}")
# 需求：读取学生数据并统计每个班级的人数

# 1、读取数据
with open("../data/student1000.txt",mode="r",encoding="utf-8") as  f:
    # 读取数据
    # print(f.readlines())
    # 使用列表推导式去处理数据
    students = [line.strip() for line in f.readlines()]
    # print(students)

# 统计每个班级学生的人数

# for line in students:
#     print(line)
# map函数
# clazz = list(map(lambda line :line.split(",")[-1],students))
# print(clazz)

# 班级
clazzs = [line.split(",")[-1] for line in students]
# print(clazzs)
# 定义一个空字典
clazz_num = {}
# 使用for循环遍历所有班级并统计班级的人数
for clazz in clazzs:
    # 判断当前班级是否存在于字典中
    if clazz not in clazz_num:
        clazz_num[clazz] = 1
    else:
        clazz_num[clazz] += 1
    print(clazz_num)
print(clazz_num)
# 1、读取数据
with open("../data/gateway_records2.txt",mode="r",encoding="utf-8") as  f:
    cars = [line.strip() for line in f.readlines()]

# 统计每个城市的车流量
citys = [line.split(",")[2] for line in cars]

city_nums = {}
for city in citys:
    if city not in city_nums:
        city_nums[city] = 1
    else:
        city_nums[city] += 1
    print(city_nums)
print(city_nums)
Hadoop介绍

Hadoop搭建

