from collections import defaultdict
import os
import re
import jieba
import codecs

def seg_word(sentence):
    """使用jieba对文档分词"""
    seg_list = jieba.cut(sentence)
    seg_result = []
    for w in seg_list:
        seg_result.append(w)
    # 读取停用词文件
    stopwords = set()
    fr = codecs.open('G:/比特币价格预测/情感词典/chineseStopWords.txt', 'r', 'gbk')
    for word in fr:
        stopwords.add(word.strip())
    fr.close()
    # 去除停用词
    seg_list0 = list(filter(lambda x: x not in stopwords, seg_result))
    return seg_list0


def list_to_dict(word_list):
    """将分词后的列表转为字典，key为单词，value为单词在列表中的索引，索引相当于词语在文档中出现的位置"""
    data = {}
    for x in range(0, len(word_list)):
        data[word_list[x]] = x
    return data


# 对分词结果分类：情感词、否定词、程度副词
# key为索引，value为权值
def classify_words(word_dict):
    # 读取情感字典文件
    sen_file = open('G:/比特币价格预测/情感词典/BosonNLP_sentiment_score.txt', 'r+', encoding='utf-8')
    # 获取字典文件内容
    # 去除'\n'
    sen_list = sen_file.read().splitlines()
    # 创建情感字典
    sen_dict = defaultdict()
    # 读取字典文件每一行内容，将其转换为字典对象，key为情感词，value为对应的分值
    for s in sen_list:
        # 每一行内容根据空格分割，索引0是情感词，索引01是情感分值
        sen_dict[s.split(' ')[0]] = s.split(' ')[1]

    # 读取否定词文件
    not_word_file = open('G:/比特币价格预测/情感词典/否定词.txt', 'r+', encoding='utf-8')
    # 由于否定词只有词，没有分值，使用list即可
    not_word_list = not_word_file.read().splitlines()

    # 读取程度副词文件
    degree_file = open('G:/比特币价格预测/情感词典/程度词.txt', 'r+', encoding='utf-8')
    degree_list = degree_file.read().splitlines()
    degree_dic = defaultdict()
    # 程度副词与情感词处理方式一样，转为程度副词字典对象，key为程度副词，value为对应的程度值
    for d in degree_list:
        #         print(d.split(',')[0],'--------',d.split(',')[1])
        degree_dic[d.split(',')[0]] = d.split(',')[1]

    # 分类结果，词语的index作为key,词语的分值作为value，否定词分值设为-1
    sen_word = dict()
    not_word = dict()
    degree_word = dict()

    # 分类
    for word in word_dict.keys():
        if word in sen_dict.keys() and word not in not_word_list and word not in degree_dic.keys():
            # 找出分词结果中在情感字典中的词
            sen_word[word_dict[word]] = sen_dict[word]  ###字典{索引;权值}
        elif word in not_word_list and word not in degree_dic.keys():
            # 分词结果中在否定词列表中的词
            not_word[word_dict[word]] = -1  ###字典{索引：-1}
        elif word in degree_dic.keys():
            # 分词结果中在程度副词中的词
            degree_word[word_dict[word]] = degree_dic[word]  ####字典{索引，权值}
    sen_file.close()
    degree_file.close()
    not_word_file.close()
    # 将分类结果返回
    #     print(sen_word, not_word, degree_word)
    return sen_word, not_word, degree_word


# 计算每个情感词得分，再相加
def socre_sentiment(sen_word, not_word, degree_word, seg_result):
    """计算得分"""
    # 权重初始化为1
    W = 1
    score = 0
    # 情感词下标初始化
    sentiment_index = -1
    # 情感词的位置下标集合
    sentiment_index_list = list(sen_word.keys())
    #     print(sentiment_index_list)
    # 遍历分词结果(遍历分词结果是为了定位两个情感词之间的程度副词和否定词)
    for i in range(0, len(seg_result)):
        # 如果是情感词（根据下标是否在情感词分类结果中判断）
        if i in sentiment_index_list:
            # 权重*情感词得分
            score += W * float(sen_word[i])
            # 情感词下标加1，获取下一个情感词的位置
            sentiment_index += 1
            if sentiment_index < len(sentiment_index_list) - 1:
                # 判断当前的情感词与下一个情感词之间是否有程度副词或否定词
                for j in range(sentiment_index_list[sentiment_index], sentiment_index_list[sentiment_index + 1]):
                    # 更新权重，如果有否定词，取反
                    if j in not_word.keys():
                        W *= -1
                    elif j in degree_word.keys():
                        # 更新权重，如果有程度副词，分值乘以程度副词的程度分值
                        W *= float(degree_word[j])
        # 定位到下一个情感词
        if sentiment_index < len(sentiment_index_list) - 1:
            i = sentiment_index_list[sentiment_index + 1]
    return score


# 主函数
# 计算得分
def setiment_score(sententce):
    # 1.对文档分词
    seg_list = seg_word(sententce)
    #     print('分词结果:',seg_list)
    # 2.将分词结果列表转为dic，然后找出情感词、否定词、程度副词
    #     print('分词字典:',list_to_dict(seg_list))
    sen_word, not_word, degree_word = classify_words(list_to_dict(seg_list))
    # 3.计算得分
    score = socre_sentiment(sen_word, not_word, degree_word, seg_list)
    return score

# 测试
if __name__ == '__main__':
    print(setiment_score("HuobiGlobal逐仓杠杆新增FLOW资产和交易"))
    print(setiment_score("太糟糕了。下雪了，摔跤了。"))
