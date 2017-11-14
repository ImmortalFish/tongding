# -*- coding: utf-8 -*-
"""
Created on Tue Nov 14 16:45:15 2017

@author: Administrator
"""

'''
处理fiber表
'''

import pandas as pd
import basic_func as bf

def HandleFiber(data, save=None, save_path=None):
    
    temp_fiber = data.copy()
    #把小写转为大写
    temp_fiber = bf.LowerToUpper(temp_fiber, '条码')
    
    #把条码分开
    temp_fiber = bf.SplitNumber(temp_fiber, '条码', split_dict={'拉丝塔号': [0,2], '光纤预制棒编号': [3,16], '大盘': [17], '小盘': [18,19]})
    
    #对每个组进行排序
    def Func(df):
        return df.sort_values(by=['条码_大盘', '条码_小盘'], ascending=[True,False])
    temp_fiber = temp_fiber.groupby('条码_光纤预制棒编号', sort=False, as_index=False).apply(Func).reset_index().drop(['level_0', 'level_1'], axis=1)
    
    #添加一列，计算各个部分的长度
    def Func_1(df):
        num = 0
        new = []
        total = df['小盘筛选长度'].sum()
        for x in df['小盘筛选长度']:
            num = x + num
            new.append(num / total)
        df['归一化'] = new
        return df
    temp_fiber = temp_fiber.groupby('条码_光纤预制棒编号', sort=False, as_index=False).apply(Func_1)
    
    if save == True:
        bf.Save(temp_fiber, save_path)
    else:
        return temp_fiber

if __name__ == '__main__':
    
    fiber = pd.read_excel('../raw_data/fiber data.xlsx')
    temp_fiber = HandleFiber(fiber, save=True, save_path='../temp_data/fiber.xlsx')