"""
1、编写一个程序，接受一系列逗号分隔的4位二进制数作为输入，然后检查它们是否可被5整除。 可被5整除的数字将以逗号分隔的顺序打印。（5分）
例：
0100,0011,1010,1001
那么输出应该是：
1010
"""
# number = input('请输入二进制数，其中用逗号隔开').split(',')
# lst = []
# for num in number:
#     if int(num,2) % 5 == 0:#转为10进制数
#         lst.append(int(num))
# print(lst)
"""
2、一个数如果恰好等于它的因子(可以被这个数整除的数)之和，这个数就称为"完数"。例如6=1＋2＋3.编程找出1000以内的所有完数。（6分）
"""

# for i in range(2,1001):
#     se = set()#因子的集合
#     for j in range(1,i):
#         if i % j == 0:
#             se.add(j)
#     if sum(se) == i:
#         print(i)

"""
4、编写一个函数 flatten_dict(d)，接受一个嵌套字典 d 作为参数，
返回一个扁平化后的字典，其中所有的键都是由原始字典的键组成的元组，以点号分隔。
例如，对于输入 {'a': 1, 'b': {'c': 2, 'd': {'e': 3}}}，
函数应该返回 {'a': 1, 'b.c': 2, 'b.d.e': 3}。（10分）
"""
#items()  函数以列表返回可遍历的(键, 值) 元组数组。
# dict.items()
#dict1.update(dict2) 将dict2中的kv对追加到dict1中

# def flatten_dict(d,parent_key = '',sep = '.'):
#     result = {}#结果字典
#     #遍历字典的kv
#     for k,v in d.items():
#         new_key = f'{parent_key}{sep}{k}' if parent_key else k
#         if type(v) == type(dict()):
#             result.update(flatten_dict(v,new_key,sep = '.'))
#         else:
#             result[new_key] = v
#     return result

# d = {'a': 1, 'b': {'c': 2, 'd': {'e': 3}}}
# print(flatten_dict(d))
