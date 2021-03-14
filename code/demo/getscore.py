from sentiment import setiment_score
import pandas as pd
import os
os.chdir(r'G:/公共卫生专项申报/数据/比特币减半')
d1=pd.read_table('第三次减半后内容.txt',header = None)
print(d1.shape)


sentiment=dict()
score=list()
for i in d1[0]:
    sen_score=setiment_score(i)
    score.append(sen_score)
sentiment['第三次减半后']=score

import json
js= json.dumps(sentiment)
f2 = open('第三次减半后情感指数.json', 'w')
f2.write(js)
f2.close()