# coding:utf8

import pandas as pd

# 生成一项候选集
def Creat_C1(item_set):
    """
    item_set是订单的集合，即由各个订单中购买商品类型的集合组成的集合。
    """
    C1 = []
    for i in item_set:
        for j in i:
            if {j} not in C1:
                C1.append(frozenset({j}))
    return C1


# 计算候选集集的支持度并选出k项频繁集
def Fre_Support_cal(D, Ck, minSupport):
    """
    输入：
    D:数据集合
    Ck：k项候选集
    minSupport：最小支持度
    输出：
    Freq_listk:k项频繁集
    support_data_dictk:k项频繁集的支持度
    """
    support_count_dictk = {}
    for raw in D:
        for item_set in Ck:
            if item_set.issubset(raw):
                if item_set not in support_count_dictk:
                    support_count_dictk[item_set] = 1
                else:
                    support_count_dictk[item_set] += 1
    num_all = len(D)
    support_data_dictk = {}
    Freq_listk = []
    for key in support_count_dictk:
        support = support_count_dictk[key] / num_all
        support_data_dictk[key] = support
        if support >= minSupport:
            Freq_listk.append(key)
    return Freq_listk, support_data_dictk


# 由k-1项频繁集生成k项候选集
def Creat_Ck(Freq_listk_1, k):
    Ck = []
    for i in range(len(Freq_listk_1)):
        for j in range(i + 1, len(Freq_listk_1)):
            if len(Freq_listk_1[i] - Freq_listk_1[j]) == 1:
                if frozenset(Freq_listk_1[i] | Freq_listk_1[j]) not in Ck:
                    Ck.append(frozenset(Freq_listk_1[i] | Freq_listk_1[j]))
    return Ck


# 生成频繁集
def func_apriori(dataset, minSupport):
    C1 = Creat_C1(dataset)
    Freq_list1, support_data_dict1 = Fre_Support_cal(dataset, C1, minSupport)
    k = 2
    Freq_listk_1 = Freq_list1
    Freq_list = []
    support_data_dict = {}
    Freq_list.extend(Freq_list1)
    support_data_dict.update(support_data_dict1)
    while k <= len(dataset):
        Ck = Creat_Ck(Freq_listk_1, k)
        Freq_listk, support_data_dictk = Fre_Support_cal(dataset, Ck, minSupport)
        Freq_list.extend(Freq_listk)
        support_data_dict.update(support_data_dictk)
        k += 1
        Freq_listk_1 = Freq_listk
    return Freq_list, support_data_dict


# 关联规则
def association_rules(freq_list, support_data_dict, min_conf):
    rules = []
    length = len(freq_list)
    for i in range(length):
        for j in range(i + 1, length):
            if freq_list[i].issubset(freq_list[j]):
                frq = support_data_dict[freq_list[j]]
                conf = support_data_dict[freq_list[j]] / support_data_dict[freq_list[i]]
                rule = (freq_list[i], freq_list[j] - freq_list[i], frq, conf)
                if conf >= min_conf:
                    print(freq_list[i], "-->", freq_list[j] - freq_list[i], 'frq:', frq, 'conf:', conf)
                    rules.append(rule)
    return rules

# 设置数据集
df_order = pd.read_csv('订单表.csv', encoding='GBK')[['客户ID','产品名称']]
dataset = df_order.groupby('客户ID').apply(lambda x: x['产品名称'].unique().tolist()).tolist()
Fre_list, support_dict = func_apriori(dataset, minSupport=0.02)
print ("以下为频繁项集：")
print (Fre_list)
print ("以下为关联规则：")
rules=association_rules(Fre_list, support_dict, min_conf=0.5)
print('Done!')
