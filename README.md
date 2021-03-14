# 数字货币金融舆情主题图谱
在非结构化文本中提取三元组
依赖于jieba分词，哈工大自然语言处理工具ltp
需要下载ltp模型文件放到./model文件夹里面
http://ltp.ai/download.html  选择 ltp_data_v3.4.0.zip

**执行步骤：**

1.	将需要提取的句子放入data/input_text.txt文件中；或者在extract_demo.py文件中的主程序块，修改输入文件的路径
2.	运行extract_demo.py
3.	将输入文件提取出的三元组输出到data/knowledge_triple.json中
4.	以管理员权限启用DOS命令行窗口，输入以下命令，通过控制台启用neo4j程序

```
neo4j.bat console
```

+ 如果看到以下消息，说明neo4j已经开始运行，启动了neo4j服务

![image-20201212144957561](C:\Users\Administrator\AppData\Roaming\Typora\typora-user-images\image-20201212144957561.png)

​	5.运行insert_to_neo4j.py 将三元组存入知识库

​	6.在浏览器中打开网址：http://localhost:7474/ ，打开neo4j浏览器界面(默认的用户是neo4j，默认的密码是：neo4j，第一次成功connect到Neo4j服务器之后，需要重置密码，本实验密码改为123456)。

​	7.在Neo4j浏览器中执行Cypher命令match (n) return n，即可查看构建的知识图谱

**Ref:** https://github.com/lemonhu/open-entity-relation-extraction

