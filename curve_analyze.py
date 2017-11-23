# -*- coding: utf-8 -*-
"""
Created on Tue Nov 21 22:59:14 2017

@author: Administrator
"""

'''
进行曲线分析
'''
import pandas as pd
import matplotlib.pyplot as plt
from scipy import optimize

def Analyze(final, change_feature=None, save=None, save_path=None):
    
    len_feature = len(change_feature)
    value_list = list(change_feature.values())
    key_list = list(change_feature.keys())
    
    #只选取final中flag为1的部分，即只分析两端的
    temp = final[final['flag'] == 1]
    
    for i in range(len_feature):
        min_num = min(value_list[i])
        max_num = max(value_list[i])
        key = key_list[i]
        
        temp = temp[(temp[key] <= max_num) & (temp[key] >= min_num)]
        
        if temp.empty:
            print('没有交集，请重新选择 %s 的区间' % key)
            break
        
    return temp

def Draw(data, target_label=None, free_feature=None):
    
    if data.empty:
        return None
    import numpy as np
    from scipy.interpolate import spline ,interp1d
    
    temp = data.sort_values(free_feature)
    temp = temp.pivot_table(index=free_feature)
    temp.reset_index(inplace=True)
    
    x = temp[free_feature]
    y = temp[target_label]
    
    f = interp1d(x, y)
    f2 = interp1d(x, y, kind='quadratic')
    xnew = np.linspace(x.min(), x.max(), num=len(x) * 6, endpoint=True)
#    plt.plot(x, y)
    plt.plot(x, y, xnew, f2(xnew), '-')
#    plt.legend(['data', 'linear', 'cubic'], loc='best')
    
#    xnew = np.linspace(x.min(),x.max(), 100)
#    power_smooth = spline(x, y, xnew)
#    plt.plot(xnew,power_smooth)
#    f1 = np.polyfit(x, y, 5)
#    p1 = np.poly1d(f1)
#    yvals = p1(x)
#    plt.plot(x, yvals, 'r')
#    plt.plot(x, y)
    
    plt.show()  
#    print(p1)
#    plt.plot(x,y)
#    plt.show()  
    
if __name__ == '__main__':
    
    final = pd.read_excel('../final_data/final_11_21.xlsx')
    target_label = '1310MFD'
    change_feature = {'pk_DeltaPlus检验值': [0.31, 0.4], 'pk_DeltaMinus检验值': [0.026, 0.028]}
    free_feature = 'ovd_密度'
    see = Analyze(final, change_feature=change_feature)
    Draw(see, target_label=target_label, free_feature=free_feature)