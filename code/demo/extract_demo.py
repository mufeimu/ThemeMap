import os
import re

import sys
sys.path.append("..")  # 先跳出当前目录
from core.nlp import NLP
from core.extractor import Extractor

import re
def filter_str(desstr,restr=','):
    #过滤除中英文及数字以外的其他字符
    res = re.compile("[^\u4e00-\u9fa5^a-z^A-Z^0-9^”^“^。^！^？^；]")
    return res.sub(restr, desstr)
# filter_str('acbdDEF哈哈哈🍕')

if __name__ == '__main__':
    # input_path = '../../data/input_text.txt'  # 输入的文本文件
    input_path = '../../data/第三次减半后内容.txt'  # 输入的文本文件
    output_path = '../../data/knowledge_triple6.json'  # 输出的处理结果Json文件

    if os.path.isfile(output_path):    ###删除指定路径下的文件
        os.remove(output_path)
    # os.mkdir(output_path)

    print('Start extracting...')

    # 实例化NLP(分词，词性标注，命名实体识别，依存句法分析)
    nlp = NLP()
    num = 1  # 知识三元组
    with open(input_path, 'r', encoding='utf-8') as f_in:
        # 分句，获得句子列表
        origin_sentences = re.split('[。？！；]|\n', f_in.read())
        # 遍历每一篇文档中的句子
        for origin_sentence in origin_sentences:
            # 原始句子长度小于2，跳过
            if (len(origin_sentence) < 2):
                continue
            # print('原始句子:',origin_sentence)
            origin_sentence=filter_str(origin_sentence)
            # print('*****')
            # print('处理句子:',origin_sentence)
            # print('type:',type(origin_sentence))
            # 分词处理 jieba分词工具
            lemmas = nlp.segment(origin_sentence)   ##分词
            # 词性标注 哈工大ltp工具
            words_postag = nlp.postag(lemmas)      ##词性标注
            # 命名实体识别 哈工大ltp工具
            words_netag = nlp.netag(words_postag)  ##命名实体识别
            # 依存句法分析 哈工大ltp工具
            sentence = nlp.parse(words_netag)      ##依存句法分析

            # print(sentence.to_string())
            extractor = Extractor()
            num = extractor.extract(origin_sentence, sentence, output_path, num)
