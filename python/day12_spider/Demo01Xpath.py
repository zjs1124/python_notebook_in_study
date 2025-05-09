"""
1、基本概念
    （1）节点（Node）
          a、元素节点：XML文档的基本构成单元，对应于xml中的标签,如：<html></html>
          b、属性节点：元素的属性，如：<ul class="xxxx">
          c、文本节点：元素或属性中的文本内容，如：<span>换一换</span>
          d、根节点：整个xml文档的根元素，如：<html></html>
          e、父节点、子节点、兄弟节点：节点之间的关系
    （2）路径表达式
         a、绝对路径：从根节点开始选择节点：如：/html/body/div/div/div/a
         b、相对路径：从当前节点开始选择节点：如：a
2、基本语法
    （1）节点选择
        a、元素节点  /html/body/div/div/div/a
        b、属性节点   /html/body/@class
        c、文本节点  /html/body/div/div/div]/a[1]/text()
    （2）运算符
        a、斜杠 / ：从根节点选取（直接找子节点）
        b、双斜杠 // ：从匹配选择的当前节点选择文档中的节点，而不考虑他们的位置（查找所有子孙节点，不考虑层级关系）
        c、点 .  ：选取当前节点
        d、双点 .. ：选取当前节点的父节点
        e、属性符号 @ ：选取属性
    （3）谓词
        a、通过位置选择
            选择第一个a标签  //div[@id='s-top-left']/a[1]
            选择最后一个a标签：//div[@id='s-top-left']/a[last()]
            选择前4个a标签： //div[@id='s-top-left']/a[position() < 4]
        b、通过属性选择
            /html/body[@class='cos-pc']/div/div[@class='s_tab']
    （4）函数
        a、字符串函数
            contains:检查字符串是否包含子字符串
            starts-with:检查字符串是否以子字符串开头
            string-length:检查字符串是否以子字符串开头
        b、数字函数
            sum：计算节点集的和
            floor：向下取整
            ceiling：向上取整
        c、布尔函数
            boolean：将值转换为布尔值
    （5）逻辑运算符
        and：用于连接两个条件，只有当两个条件都为真时才返回真
        or ：用于连接两个条件，只要有一个条件为真，则返回真
        not ：用于返回条件的否定

"""