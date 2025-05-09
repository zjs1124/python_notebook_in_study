"""
1、编写一个函数，接受一个列表并返回该列表的所有子列表。[1, 2, 3]
2、 如何使用列表推导式生成一个包含前 100 个平方数的列表？
3、如何将元组 (1, 2, 3) 的每个元素分别赋值给变量 a, b, c？
4、编写一个函数，统计字符串中每个字符的出现次数。   "hello"
5、如何合并两个字典 {'a': 1, 'b': 2} 和 {'b': 3, 'c': 4}，若键重复则值相加？
6、编写一个函数process_data，它接受一个包含字典的列表作为输入。每个字典表示一个学生的成绩数据，其中包含学生的姓名、学科及其分数。函数应该返回一个包含元组的列表，每个元组包含学生的姓名、总分和平均分。
students = [
    {"name": "Alice", "subject": "Math", "score": 90},
    {"name": "Alice", "subject": "English", "score": 85},
    {"name": "Bob", "subject": "Math", "score": 78},
    {"name": "Bob", "subject": "English", "score": 82},
    {"name": "Charlie", "subject": "Math", "score": 88},
    {"name": "Charlie", "subject": "English", "score": 90}
]
7、编写一个函数analyze_text，该函数接受一个字符串作为输入，返回一个包含四个元素的元组，分别是：
字符串中单词的集合。
每个单词在字符串中出现的次数的字典。
最长的单词及其长度。
按出现次数排序的单词列表。
text = "this is a test. this test is only a test."
8、编写一个函数combine_collections，该函数接受多个参数，每个参数可以是列表、元组或集合。函数应将所有参数合并成一个集合，并返回包含以下信息的字典：
合并后的集合。
集合中元素的总数。
集合中最常见的元素及其出现次数（如果有多个，返回任意一个）。
result = combine_collections([1, 2, 3], {2, 3, 4}, (4, 5, 6), [4, 1, 2])

9、编写一个函数nested_structure_analysis，它接受一个包含任意层次嵌套的列表或元组，并返回一个字典，字典的键是数据类型，值是该类型在整个嵌套结构中出现的次数。
nested_data = [1, (2, 3, [4, (5, 6)]), {7, 8, (9, 10)}]
10、编写一个函数transform_and_filter，它接受一个字典列表和一个过滤函数作为参数。函数应对字典中的每个值应用过滤函数，并返回一个新的字典列表，其中只包含过滤函数返回True的键值对。
data = [
    {"name": "Alice", "age": 28, "score": 85},
    {"name": "Bob", "age": 22, "score": 78},
    {"name": "Charlie", "age": 25, "score": 92}
]
filter_fn = lambda x: isinstance(x, int) and x > 80
result = transform_and_filter(data, filter_fn)

"""
#1、编写一个函数，接受一个列表并返回该列表的所有子列表。[1, 2, 3]
#[i:j:?]
# def child_list(lst):
#     l = []#创建空列表
#     l_set = []#创建相同的列表
#     # for i in l:
#     #     l.append([l[i]])#全部单个数
#     for i in range(len(lst)):
#         for j in range(1,len(lst)+1):
#             for z in range(1,len(lst)):#步长为1
#             # l.append(lst[i:i+j])
#                 l.append(lst[i:i+j:z])
#     print(l)
#     for i in l:
#         while(l.count(i) >= 2):
#                 l.remove(i)
#     print(l)
#     #找到重复的
#     # for i in range(len(l)-1):
#     #     if l[i] == l[i+1]:
#     #         l_set.append(i)
#     # print(l_set)
#     # #去重
#     # l_set.reverse()
#     # for i in(l_set):
#     #     l.pop(i)
#     # print(l)
#     # set.add(l[0])
#     # print(set)
#     # return l





# ls = [1,2,3]
# print(child_list(ls))
#2、 如何使用列表推导式生成一个包含前 100 个平方数的列表？
# l = [ i ** 2 for i in range(1,101)]
# print(l)

#3、如何将元组 (1, 2, 3) 的每个元素分别赋值给变量 a, b, c？
# tuple = (1, 2, 3)
# a  = tuple[0]
# b = tuple[1]
# c = tuple[2]
# print(a)
# print(b)
# print(c)

#4、编写一个函数，统计字符串中每个字符的出现次数。   "hello"
# s =  "hello"
# l = []
# for i in s:
#     l.append(s.count(i))
# print(l)

#5、如何合并两个字典 {'a': 1, 'b': 2} 和 {'b': 3, 'c': 4}，若键重复则值相加？
# d = {'a': 1, 'b': 2}
# b = {'b': 3, 'c': 4}
# for key in b.keys():
#     if key in d.keys():
#         d[key] = d[key] + b[key]
#     else:
#         d[key] = b[key]
# print(d)

"""
6、编写一个函数process_data，它接受一个包含字典的列表作为输入。每个字典表示一个学生的成绩数据，其中包含学生的姓名、学科及其分数。函数应该返回一个包含元组的列表，每个元组包含学生的姓名、总分和平均分。
students = [
    {"name": "Alice", "subject": "Math", "score": 90},
    {"name": "Alice", "subject": "English", "score": 85},
    {"name": "Bob", "subject": "Math", "score": 78},
    {"name": "Bob", "subject": "English", "score": 82},
    {"name": "Charlie", "subject": "Math", "score": 88},
    {"name": "Charlie", "subject": "English", "score": 90}
]
"""
# def process_data(lst):
#     l = []
#     sum = 0
#     count = 1
#     sum = lst[0]['score']
#     for i in range(len(lst)-1):
        
#         if lst[i]['name'] == lst[i + 1]['name']:
#             sum += lst[i+1]['score']
#             print(sum)
#             count += 1
#             l.append((lst[i]['name'],sum,sum / count))
#         else:
#             # l.append((lst[i]['name'],sum,sum / count))
#             sum = lst[i+1]['score']
#             count = 1
#     return l

# dic_lst = [
#     {"name": "Alice", "subject": "Math", "score": 90},
#     {"name": "Alice", "subject": "English", "score": 85},
#     {"name": "Bob", "subject": "Math", "score": 78},
#     {"name": "Bob", "subject": "English", "score": 82},
#     {"name": "Charlie", "subject": "Math", "score": 88},
#     {"name": "Charlie", "subject": "English", "score": 90}
# ]
# print(process_data(dic_lst))

"""
7、编写一个函数analyze_text，该函数接受一个字符串作为输入，返回一个包含四个元素的元组，分别是：
字符串中单词的集合。
每个单词在字符串中出现的次数的字典。
最长的单词及其长度。
按出现次数排序的单词列表。
text = "this is a test. this test is only a test."
"""
# def analyze_text(s):
#     dic = {}#每个单词在字符串中出现的次数的字典
#     longst = 1#最长单词长度
#     longst_string = []#最长单词的列表
#     appear = []#出现次数
#     appear_string = []#按出现次数排序的单词列表
#     string = None#最长的字符串
#     result = []
#     l = s.strip('.').split(' ')
#     # print(l)
#     for i in range(len(l)):
#         if '.' in l[i]:
#             l[i] = l[i].replace('.','')
#     # print(l)
#     #字符串中单词的集合。
#     se = set(l)
#     # print(se)
#     #每个单词在字符串中出现的次数的字典。
#     for i in l:
#         dic[i] = l.count(i)
#     # print(dic)
#     #最长的单词及其长度。
#     for i in range(len(l) - 1):
#         if len(l[i]) >= longst:
#             longst = len(l[i])
#             string = l[i]
#             longst_string.append(string)
#         else:
#             continue
#     # longest_string = set(longest_string)
#     # print(longst_string)
#     # print(longst)
#     #按出现次数排序的单词列表
#     for key in dic.keys():
#         appear.append(dic[key])
#     # print(appear)
#     appear = list(set(appear))
#     appear.sort(reverse = True)
#     # print(appear)
#     for i in appear:
#         for key in dic.keys():
#             if(i == dic[key]):
#                 appear_string.append(key)
#     # print(appear_string)
#     result.append(se)
#     result.append(dic)
#     result.append(longst)
#     result.append(longst_string)
#     result.append(appear_string)
#     result = tuple(result)

#     return result

# text = "this is a test. this test is only a test."
# print(analyze_text(text))

"""
8、编写一个函数combine_collections，该函数接受多个参数，每个参数可以是列表、元组或集合。函数应将所有参数合并成一个集合，并返回包含以下信息的字典：
合并后的集合。
集合中元素的总数。
集合中最常见的元素及其出现次数（如果有多个，返回任意一个）。
result = combine_collections([1, 2, 3], {2, 3, 4}, (4, 5, 6), [4, 1, 2])
"""
# def combine_collections(*args):#传入为一个元组
#     dic = {}
#     # print(args)
#     #合并后的集合。
#     se = set()
#     for i in args:
#         if type(i) == type(list()):
#             i = tuple(i)
#         if type(i) == type(set()):
#             i = tuple(i)
#         se.add(i)
#     # print(se)
#     #集合中元素的总数
#     length = len(se)
#     # print(length)
#     #集合中最常见的元素及其出现次数（如果有多个，返回任意一个
#     total = []
#     for i in se:
#         total.extend(i)
#     # print(total)
#     longest = 1
#     longest_number = 0
#     for i in total:
#         if total.count(i) >= longest:
#             longest = total.count(i)
#     for i in total:
#         if total.count(i) == longest:
#             longest_number = i
#             break
#     # print(longest_number)
#     dic['合并后的集合'] = se
#     dic['集合中元素的总数'] = length
#     dic['集合中最常见的元素及其出现次数'] = longest_number
#     return dic



# result = combine_collections([1, 2, 3], {2, 3, 4}, (4, 5, 6), [4, 1, 2])
# print(result)


"""
9、编写一个函数nested_structure_analysis，它接受一个包含任意层次嵌套的列表或元组，并返回一个字典，字典的键是数据类型，值是该类型在整个嵌套结构中出现的次数。
nested_data = [1, (2, 3, [4, (5, 6)]), {7, 8, (9, 10)}]
"""

# list_count = 0
# tuple_count = 0
# set_count = 0
# new = []#没有嵌套的
# old = []#有嵌套的
# def nested_structure(lst):
#     se ={1}
#     for i in range(len(lst)):
#         if type(lst[i]) == type(list()):
#             global list_count
#             list_count += 1
#             nested_structure_analysis(lst[i])
#         elif type(lst[i]) == type(tuple()):
#             global tuple_count 
#             tuple_count += 1
#             nested_structure_analysis(lst[i])
#         elif type(lst[i]) == type(se):
#             lst[i] = tuple(lst[i])
#             global set_count
#             set_count += 1
#             nested_structure_analysis(lst[i])
#         else:
#             new.append(lst[i])
#     return new
    
# def nested_structure_analysis(l):
#     nested_structure(l)
#     dic = {}
#     dic['list'] = list_count 
#     dic['tuple'] = tuple_count
#     dic['set'] = set_count
#     return dic

# nested_data = [1, (2, 3, [4, (5, 6)]), {7, 8, (9, 10)}]
# print(nested_structure_analysis(nested_data))

"""
10、编写一个函数transform_and_filter，它接受一个字典列表和一个过滤函数作为参数。函数应对字典中的每个值应用过滤函数，并返回一个新的字典列表，其中只包含过滤函数返回True的键值对。
data = [
    {"name": "Alice", "age": 28, "score": 85},
    {"name": "Bob", "age": 22, "score": 78},
    {"name": "Charlie", "age": 25, "score": 92}
]
filter_fn = lambda x: isinstance(x, int) and x > 80
result = transform_and_filter(data, filter_fn)
"""

# def transform_and_filter(lst,filter):
#     l = []
#     dic = {}
#     for i in range(len(lst)):
#         dic['name'] = filter(lst[i]['name'])
#         dic['age'] = filter(lst[i]['age'])
#         dic['score'] = filter(lst[i]['score'])
#         l.append(dic)
#     return l


# data = [
#     {"name": "Alice", "age": 28, "score": 85},
#     {"name": "Bob", "age": 22, "score": 78},
#     {"name": "Charlie", "age": 25, "score": 92}
# ]
# filter_fn = lambda x: isinstance(x, int) and x > 8
# result = transform_and_filter(data, filter_fn)
# print(result)