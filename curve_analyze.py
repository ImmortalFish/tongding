# -*- coding: utf-8 -*-
"""
Created on Tue Nov 21 22:59:14 2017

@author: Administrator
"""

'''
进行曲线分析
'''
import pandas as pd
import basic_func as bf
from intervals import Interval
import matplotlib.pyplot as plt
    

def Analyze(final, change_feature=None, save=None, save_path=None):
    
    #只选取final中flag为1的部分，即只分析两端的
    final_1 = final[final['flag'] == 1]
    
    #先取change_feature的第一个特征
    min_num = min(list(change_feature.values())[0])
    max_num = max(list(change_feature.values())[0])
    key = list(change_feature.keys())[0]
    temp = final_1[(final_1[key] <= max_num) & (final_1[key] >= min_num)]
    
    #获得下一个特征的最大最小值
    key = list(change_feature.keys())[1]
    min_num = temp[key].min()
    max_num = temp[key].max()
    
    #再取change_feature的第二个特征
    interval_1 = Interval([min_num, max_num])
    min_num = min(list(change_feature.values())[1])
    max_num = max(list(change_feature.values())[1])
    interval_2 = Interval([min_num, max_num])
    
    try:
        jiaoji = interval_1 & interval_2
        min_num = jiaoji.lower
        max_num = jiaoji.upper
        temp = final_1[(final_1[key] <= max_num) & (final_1[key] >= min_num)]
    except Exception as e:
        print('没有交集，请重新选择上一个特征的区间')
    
    return temp

def Draw(data, target_label=None, free_feature=None):
    
    temp = data.sort_values(free_feature)
    temp = temp.pivot_table(index=free_feature)
    temp.reset_index(inplace=True)
    
    x = temp[free_feature]
    y = temp[target_label]
    plt.plot(x,y)
    plt.show()  
    
if __name__ == '__main__':
    
    final = pd.read_excel('../final_data/final_11_21.xlsx')
    target_label = '1310MFD'
    change_feature = {'pk_DeltaPlus检验值': [0.31, 0.4], 'pk_DeltaMinus检验值': [0.026, 0.0265]}
    free_feature = 'ovd_密度'
    see = Analyze(final, change_feature=change_feature)
    Draw(see, target_label=target_label, free_feature=free_feature)