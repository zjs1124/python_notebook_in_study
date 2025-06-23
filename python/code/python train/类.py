
#封装1
# class Phone:
#     num = None
#     brand = None
#     price = None

#     __volt = None

#     def play_games(self):
#         print("正在打游戏")
    
#     def __control(self):
#         print("程序调度")
    
#     def volt(self):
#         self.__volt = '220V'
#         print(f'电压为：{self.__volt}')

# iphone = Phone()
# iphone.brand = 5
# print(iphone.brand)#5
# iphone.play_games()#正在打游戏
# iphone.volt()#电压为：220V
# Phone.__volt = 5
# print(Phone.__volt)#python自己创建的临时变量，虚假的。没有修改类里面的私有属性
# phone.__control()#AttributeError: type object 'phone' has no attribute '__control'

"""
练习：设计带有私有成员的手机

设计一个手机类，内部包含：
私有成员变量：__is_5g_enable,bool类型，True表示开启5g，False表示关闭5g
私有成员方法：__check_5g() 会判断私有成员变量__is_5g_enable的值
    如果为True，打印开启5g
    如果为False，关闭5g
共开的成员变量：手机序列号、手机价格
共开的成员方法：call_by_5g()、play_game()
    call_by_5g调用私有成员方法__check_5g()，判断5g的状态
    打印输出结果：正在通话中
运行结果：
    5g关闭，使用4g网络
    正在通话中
"""
# class Phone:
#     __is_5g_enable = True

#     id = None
#     price = None

#     def __check_5g(self):
#         if self.__is_5g_enable:
#             print("打开5g")
#         else:
#             print("关闭5g")

#     def call_by_5g(self):
#         self.__check_5g()
#         print("正在通话中")


#     def play_game(self):
#         pass

# oppo = Phone()
# oppo.call_by_5g()

"""
打开5g
正在通话中
"""
"""
继承（单继承,多继承）
"""
# #父类
# class Phone:
#     id = 'oppo'
#     price = '5000'

#     def play_5g(self):
#         print('5g打游戏')

# class Phone1:
#     id = 'Mi'
#     price = '6000'
#     generations = 11

#     def play_5g(self):
#         print('4g打游戏')
    
#     def video(self):
#         print('2k大屏')
# #子类
# class Phone3(Phone):
#     pass

# class Phone4(Phone,Phone1):
#     pass


# oppo = Phone3()
# print(oppo.id)
# print(oppo.price)
# oppo.play_5g()

# oneplus = Phone4()
# print(oneplus.id)
# print(oneplus.price)
# oneplus.play_5g()
# oneplus.video()
"""
oppo
5000
5g打游戏
oppo
5000
5g打游戏
2k大屏
"""
#yield关键词

# def number():
#     x = 5
#     yield x + 1
#     yield x + 2
#     x + 5

# num = number()
# print(next(num))# 6 
# print(next(num))# 7
# print(next(num))#StopIteration 结束前都没有遇到yield关键字，直到遇到函数结束，报错

#注解

# def func(x:int,y:int) -> int:
#     pass

# a:int = 1
# b:str = 'str'
# l:list[int] = [1,2,3]
# t:tuple[int,str,list] = (1,'2',[1,2,3])#要对元组里面的元素依次进行注解
# dic:dict[str,int] = {'age':18}
# se:set[int] = {1,2,3}

# class Phone:
#     pass

# iphone:Phone = Phone()#类对象进行注解

# a = 1 #type:int

# from typing import Union

# l:list[Union[int,str]] = [1,2,3,'z']

# dic:dict[str,Union[str,int]] =  {'name':'str','age' : 1}

# def func(data:Union[str,int]) -> Union[str,int]:
#     pass
# func()

#多态

class Animals:
    # id = 5
    def spark(self):#抽象类
        pass    #抽象方法

class Cat(Animals):
    # id = 2
    def spark(self):
        print("miao miao")
        Animals.spark(self)
        super().spark()
        # print(super().id)
        # print(Animals.id)

class Dog(Animals):
    def spark(self):
        print("go go")

def main(anm:Animals):
    anm.spark()

dog = Dog()
cat = Cat()
# main(dog)
# main(cat)
cat.spark()
dog.spark()


