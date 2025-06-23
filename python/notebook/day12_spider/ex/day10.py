"""
1、匹配邮箱地址
编写一个正则表达式，用于匹配有效的邮箱地址。邮箱地址的格式应为：用户名@域名.顶级域名，用户名可以包含字母、数字、点和下划线，域名和顶级域名只能包含字母和数字。
test_emails = ["test.email@example.com", "invalid-email@.com", "user_name@domain.co", "user@domain.c"]

2、提取电话号码
编写一个正则表达式，从文本中提取所有的电话号码。电话号码的格式为：可以包含括号的区号（如(123)或123），然后是一个三位数和四位数的组合，中间可以用空格或连字符分隔。
text = "Contact us at (123) 456-7890 or 123-456-7890 or 123 456 7890."

3、验证IP地址
编写一个正则表达式，用于验证IPv4地址。IPv4地址的格式为四个0到255之间的数字，用点分隔。
test_ips = ["192.168.1.1", "256.256.256.256", "123.045.067.089", "172.16.254.1"]

4、匹配日期格式
编写一个正则表达式，用于匹配日期，日期格式为YYYY-MM-DD。确保年是四位数，月和日是两位数。
test_dates = ["2024-06-22", "2024-6-2", "2024/06/22", "2024-12-01"]

5、查找重复单词
编写一个正则表达式，从文本中查找并提取所有重复出现的单词（忽略大小写）。
text = "Lanzhi shujia shujia Lanzhi Python python"

6、实现一个银行账户类
要求：
创建一个类 BankAccount，具有以下属性：
    account_number: 账户号码（字符串）
    balance: 余额（浮点数）
创建以下方法：
    deposit(amount): 存款，增加余额
    withdraw(amount): 取款，减少余额，确保余额不小于取款金额，否则显示错误信息
    display_balance(): 显示当前余额

7、实现一个员工和经理类
要求：
创建一个基类 Employee，具有以下属性：
    name: 姓名（字符串）
    salary: 工资（浮点数）
创建以下方法：
    work(): 显示员工在工作
    display_info(): 显示员工姓名和工资
创建一个派生类 Manager，继承自 Employee，并增加以下属性：
    bonus: 奖金（浮点数）
重写 display_info 方法以显示经理的姓名、工资和奖金
"""

"""
1、匹配邮箱地址
编写一个正则表达式，用于匹配有效的邮箱地址。邮箱地址的格式应为：用户名@域名.顶级域名，用户名可以包含字母、数字、点和下划线，域名和顶级域名只能包含字母和数字。
test_emails = ["test.email@example.com", "invalid-email@.com", "user_name@domain.co", "user@domain.c"]
"""
# import re
# test_emails ='"test.email@example.com", "invalid-email@.com", "user_name@domain.co", "user@domain.c"'
# rt = re.findall(r'[a-zA-Z0-9._]+@[a-zA-z0-9]+.[a-zA-Z0-9]+',test_emails)
# print(rt)

"""
2、提取电话号码
编写一个正则表达式，从文本中提取所有的电话号码。电话号码的格式为：可以包含括号的区号（如(123)或123），然后是一个三位数和四位数的组合，中间可以用空格或连字符分隔。
text = "Contact us at (123) 456-7890 or 123-456-7890 or 123 456 7890."
"""
# import re
# text = "Contact us at (123) 456-7890 or 123-456-7890 or 123 456 7890."
# rt = re.findall(r'[\\(]?\d+[\\)]?[\s-]?[\d]{3,4}[\s-]?[\d]{3,4}',text)
# print(rt)

"""
# 3、验证IP地址
# 编写一个正则表达式，用于验证IPv4地址。IPv4地址的格式为四个0到255之间的数字，用点分隔。
# test_ips = ["192.168.1.1", "256.256.256.256", "123.045.067.089", "172.16.254.1"]
# """
# import re
# test_ips = '"192.168.1.1", "256.256.256.256", "123.045.067.089", "172.06.254.1"'
# rt = re.findall(r'(?:[2][5][0-5]|[2][0-4][0-9]|[1][0-9][0-9]|[1]?[1-9]?[0-9])[.](?:[2][5][0-5]|[2][0-4][0-9]|[1][0-9][0-9]|[1]?[1-9]?[0-9])[.](?:[2][5][0-5]|[2][0-4][0-9]|[1][0-9][0-9]|[1]?[1-9]?[0-9])[.](?:[2][5][0-5]|[2][0-4][0-9]|[1][0-9][0-9]|[1]?[1-9]?[0-9])',test_ips)
# print(rt)

"""
4、匹配日期格式
编写一个正则表达式，用于匹配日期，日期格式为YYYY-MM-DD。确保年是四位数，月和日是两位数。
test_dates = ["2024-06-22", "2024-6-2", "2024/06/22", "2024-12-01"]
"""
# import re
# test_dates = '"2024-06-22", "2024-6-2", "2024/06/22", "2024-12-01"'
# rt = re.findall(r'\d{4}[-]\d{2}[-]\d{2}',test_dates)
# print(rt)

"""
*** 5、查找重复单词
编写一个正则表达式，从文本中查找并提取所有重复出现的单词（忽略大小写）。
text = "Lanzhi shujia shujia Lanzhi Python python"
"""
# import re
# text = "Lanzhi shujia shujia Lanzhi Python python"
# rt = re.findall(r'(\b\w+\b)',text)
# print(rt)

"""
6、实现一个银行账户类
要求：
创建一个类 BankAccount，具有以下属性：
    account_number: 账户号码（字符串）
    balance: 余额（浮点数）
创建以下方法：
    deposit(amount): 存款，增加余额
    withdraw(amount): 取款，减少余额，确保余额不小于取款金额，否则显示错误信息
    display_balance(): 显示当前余额
"""

# class BankAccount:
#     #账户号码
#     account_number:str = None
#     #余额
#     balance:float = None
#     #增加余额
#     def deposit(self,amount):
#         self.balance = self.balance + amount
#         print(f'成功存款')
#         self.display_balance()
#     #取款，减少余额，确保余额不小于取款金额，否则显示错误信息
#     def withdraw(self,amount):
#         if amount > self.balance:
#             print(f"余额不足")
#             self.display_balance()
#         else:
#             self.balance = self.balance - amount
#             print(f'取款成功')
#             self.display_balance()
#     #显示当前余额
#     def display_balance(self):
#         print(f'您当前余额为:{self.balance}')


# a = BankAccount()
# a.account_number = input('输入您的账户号码:')
# print(a.account_number)
# a.balance = float(input("请输入您的余额："))
# a.display_balance()
# a.deposit(float(input("您想存入的余额为:")))
# a.withdraw(float(input("您想取出的余额为:")))
# a.display_balance()

"""
7、实现一个员工和经理类
要求：
创建一个基类 Employee，具有以下属性：
    name: 姓名（字符串）
    salary: 工资（浮点数）
创建以下方法：
    work(): 显示员工在工作
    display_info(): 显示员工姓名和工资
创建一个派生类 Manager，继承自 Employee，并增加以下属性：
    bonus: 奖金（浮点数）
重写 display_info 方法以显示经理的姓名、工资和奖金
"""
# class Employee:
#     name:str = None
#     salary:float = None

#     #显示员工在工作
#     def work(self):
#         print(f'work work')
#         print(f'work work')
#         print(f'work work')
#         print(f'work work')
#         print(f'勤劳又勇敢的血狼破军')
#         print(f'为了团队的刷铁机')
#         print(f'他做出了巨大的贡献')
#         print(f'巨大的carry')
#         print(f'无敌了')
#         print(f'无敌了')

#     #显示员工姓名和工资
#     def display_info(self):
#         print(f'员工的姓名为：{self.name}')
#         print(f'员工的工资为为：{self.salary}')

# class Manager(Employee):
#     bonus:float = None

#     #显示经理的姓名、工资和奖金
#     def display_info(self):
#         print(f'经理的姓名为：{self.name}')
#         print(f'经理的工资为：{self.salary}')
#         print(f'经理的奖金为为：{self.bonus}')


# em = Employee()
# em.name = input("请输入您的姓名（员工）:")
# em.salary = input("请输入您的工资(员工):")
# em.display_info()
# em.work()
# ma = Manager()
# ma.name = input("请输入您的姓名（经理）:")
# ma.salary = input("请输入您的工资(经理):")
# ma.bonus = input("请输入您的奖金(经理):")
# ma.display_info()

