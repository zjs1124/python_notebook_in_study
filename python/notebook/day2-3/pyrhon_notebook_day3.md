### 数据输入

1. 函数：input()函数,用来获取来自键盘的输入
2. 语法：x = input("str") # input()函数传入的数据的数据类型为字符串类型

### 判断语句

1. if语句，语法：
```python
 if 判断条件：（其中判断条件返回的值为bool类型，也就是True/False）  
           判断条件成立时执行的语句 
    elif 判断条件: （非必须需要写） 
           判断条件成立时执行的语句
    elif 判断条件: （非必须需要写）
            判断条件成立时执行的语句
    else:    （非必须需要写）
            上述判断条件都不成立时执行的语句
```

2. 判断嵌套：
```python
   if 判断条件：
      判断语句（可以省略，直接写if判断语句）
      if 判断条件：
        判断语句
```

### 循环语句

1. while循环语法：
```python
   while 循环条件：
      循环体 （当循环条件成立时执行）
``` 
  while循环执行时要设置循环的终止条件  


1. for循环：是一种轮询的机制，是对一批内容进行逐个处理。
   
  语法：
  ```python
     for 临时变量 in 数据集合：
       循环体  
   ```
  其中临时变量在编程规范上只会在for循环里面才可以调用，但实际上却可以在外面调用。但应尽量避免。如需调用，则应该在外部事先定义好变量。

3. range函数：
  格式：
  ```python
  range(num1,num2,step)  从num1到num2(不包括num2),步长为setp
  ```
  其中num1默认为0,step默认为1，步长为-1时则减号

4. 循环嵌套：
for 和 while循环可以相互嵌套：
eg:
for&for 循环
```python
    for i in range(10):
        for j in range(10):
            print(j)
```
while&while循环
```python
    i = 0
    j = 0
    while(i<=10):
        while(j<=10):
            print(j)
            j += 1
        i += 1    
```
for&while循环：
```python
    j = 1
    for i in range(10):
        while(j <= 10):
            print(j)
            j += 1
```
while&for 循环：
```python
    i = 0
    while(i<=10)
        for j in range(10):
            print(j)
        i += 1
```


 1. 循环中止
 continue:中止本次循环，执行下次的循环
 eg:
 ```python
    for i in range(10):
        for j in range(10):
            print(j)
            continue
            print("111") #结果只有数字 而不会出现111
 ```  
 break:跳出本次循环，不再执行后面的循环
```python
    for i in range(10):
        for j in range(10):
            print(j)
            break #只会输出多个0
```
   
