# coding:utf8

import requests
import re
import pandas as pd
url='http://car.bitauto.com/xuanchegongju/?l=8&mid=8'
response=requests.get(url)
if response.status_code==200:
    text=response.text
    pattern1 = re.compile('p class="cx-name text-hover">(.*?)</p>')
    temp_lst1 = re.compile(pattern1).findall(response.text)
    pattern2 = re.compile('<p class="cx-price">(.*?)</p>')
    temp_lst2 = re.compile(pattern2).findall(response.text)
    pattern3 = re.compile('<img class="img" src="(.*?)"')
    temp_lst3 = re.compile(pattern3).findall(response.text)
    df=pd.DataFrame([temp_lst1,temp_lst2,temp_lst3]).T
    df.columns=['名称','价格','产品图片链接']
    df['产品图片链接']=df['产品图片链接'].map(lambda x:'http:'+x)
    df['最低价格']=df['价格'].map(lambda x:x.split('-')[0])
    df['最低价格']=df['最低价格'].map(lambda x:str(x)+'万' if x!='暂无' else x)
    df['最高价格'] = df['价格'].map(lambda x: x.split('-')[-1])
    df=df.drop('价格',axis=1)
    df.set_index('名称').to_csv('采集大众品牌SUV汽车报价.csv',encoding='gbk')
else:
    print ('error')