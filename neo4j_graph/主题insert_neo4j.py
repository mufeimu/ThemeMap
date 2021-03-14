from neo4j import GraphDatabase
import json

topic=[
    '疯狂', '央行', '金融', '美元', '英国', '减半', '交易','暴涨', '产量', '被盗',
    '行情','投资','区块链', '成交价', '研究','技术', '震荡', '支付', '新高', '中国',
    '止损', '公司', '交易所', '虚拟','币',   '用户', '币圈', '涨幅', '数据','市场',
    '比特币', '僵尸','分析', '监控', '价格', '加密', '数字','货币', '未来','制造',
    ]


driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "123456"))
# driver = GraphDatabase.driver("https://localhost:7474", auth=("neo4j", "neo4j"))


###添加节点和关系,节点属性为name
# def add_node(tx, name1, relation,name2):
#     tx.run("MERGE (a:Node{name: $name1}) "    ###创建实体，标签是Node，属性是name，节点名是a；图谱显示的是属性name
#         "MERGE (b:Node{name: $name2}) "
#            "MERGE (a)-[:"+relation+"]-> (b)",###创建关系，
#            name1=name1,name2=name2)

###添加节点和关系,节点属性为name
def add_node(tx, name1, relation,name2):
    tx.run("MERGE (a:Node{name: $name1}) "    ###创建实体，标签是Node，属性是name，节点名是a；图谱显示的是属性name
        "MERGE (b:Node{name: $name2}) "
           "MERGE (a)-[:"+relation+"]-> (b)",###创建关系，
           name1=name1,name2=name2,relation=relation)


"""
清洗整理三元组  
"""
####先筛选出正常三元组，后按主题词筛选出主题三元组，再进行三元组分配

###判断字符串中是否有除中英文及数字外的其他任何字符  函数
import re
def find_emoji(emoji_str):
    #过滤除中英文及数字以外的其他字符
#     res = re.compile("[^\u4e00-\u9fa5^a-z^A-Z^0-9]")   ###匹配非中英文及数字
    ##过滤非中文字符
    res = re.compile("[^\u4e00-\u9fa5]")  ###匹配非中文
    return res.search(emoji_str)

lines=open('../data/knowledge_triple5.json','r',encoding='utf-8-sig').readlines()
triples1=[]
for line in lines:
    line=json.loads(line)
    triples1.append(tuple(line['知识']))
print('提取的三元组数量:',len(triples1))
triples=list(set(triples1))   ##存放无重复的三元组
print('去重后三元组数量:',len(triples))

"""
三元组分配，加入neo4j
"""
with driver.session() as session:
    # lines=open('../data/knowledge_triple.json','r',encoding='utf-8').readlines()  #原代码
    pattern=''
    n=0
    m=0
    temp=0
    delete=['他们','这样','我们','您好','有人','时候','微博视频','全文','网页','链接']
    for i, triple in enumerate(triples):
        for j in triple:
            if find_emoji(j) or j in delete or len(j)<2:
                temp=1
                m+=1
                break
        if temp==1:
            temp=0
            continue
        for j in triple:
            if j in topic:
                # print(triple)
                name1 = triple[0]  ###头实体
                relation = triple[1]##关系
                name2 = triple[2]  ##尾实体
                print(str(i + 1))
                n+=1
                try:
                    session.write_transaction(add_node, name1, relation, name2)
                except Exception as e:
                    pass
                    # print(name1, relation, name2, str(e))
                break
    print('无意义的三元组数量:',m,'\n最终有效主题三元组数量:',n)

###设计一个筛选机制，将三元组中含有标点符号、方框等不规范的关系的三元组删去