#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2025/3/22 22:07
# @Author  : A

import pymysql
import pandas as pd
# 数据库连接配置
config = {
    'user': 'root',
    'password': '123456',
    'host': 'master',
    'database': 'car_data',
    'charset': 'utf8mb4'
}
try:
    connection = pymysql.connect(**config)
    cursor = connection.cursor()
except pymysql.Error as err:
    print(f"数据库连接失败: {err}")
# 定义 CSV 文件路径和对应的表名
files = {
    'data/car_beijing.csv': 'car_beijing','data/car_hangzhou.csv': 'car_hangzhou','data/car_hefei.csv': 'car_hefei','data/car_nanjing.csv': 'car_nanjing',
    'data/car_shanghai.csv': 'car_shanghai'
}
# 遍历文件并将数据插入相应的表中
for file_path, table_name in files.items():
    try:
        df = pd.read_csv(file_path)
        columns = ', '.join(df.columns)
        placeholders = ', '.join(['%s'] * len(df.columns))
        insert_query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        for row in df.values.tolist():
            cursor.execute(insert_query, row)
        connection.commit()
        print(f"{file_path} 数据已成功插入 {table_name} 表")
    except pymysql.Error as err:
        print(f"插入 {file_path} 数据时出错: {err}")
        connection.rollback()
    except FileNotFoundError:
        print(f"文件 {file_path} 未找到")
# 关闭游标和连接
cursor.close()
connection.close()

