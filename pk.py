# -*- coding: utf-8 -*-
"""
Created on Tue Nov 14 14:25:19 2017

@author: Administrator
"""

'''
处理合并后的pk表
'''

import pandas as pd
import basic_func as bf

def ExpandPk(pk, save=None, save_path=None):

    temp_pk = pk.copy()
    
    #删除空行和空列
    temp_pk.dropna(axis=0, how='all', inplace=True)
    temp_pk.dropna(axis=1, how='all', inplace=True)
    
    #删除无关的列
    drop_list = ['单据编号', '状态', '操作人', '操作日期', '班组代码',
                     '班组名称', '职员代码', '设备名称']
    temp_pk.drop(drop_list, axis=1, inplace=True)
    
    #删除异常的芯棒编码
    temp_pk = bf.Del(temp_pk, '芯棒编码')
    
    #把平均值换成数值
    def Func(df):
        df['新位置'] = df['位置']
        if '平均值' in df['位置'].values:
            mean_num = int(df['位置'][:-1].astype('int').mean())
            df['新位置'].replace('平均值', mean_num, inplace=True)
            df['新位置'] = df['新位置'].astype('int')
        return df
    temp_pk = temp_pk.groupby('芯棒编码', sort=False, as_index=False).apply(Func)
    
    #添加归一化列
    def Func_1(df):
        df['归一化'] = [int(x) / int(df['新位置'].max()) for x in df['新位置']]
        return df
    temp_pk = temp_pk.groupby('芯棒编码', sort=False, as_index=False).apply(Func_1)
    
    #重命名列名
    temp_pk = bf.Rename(temp_pk, prefixes='pk')
    
    #保存处理后的文件
    if save == True:
        bf.Save(temp_pk, save_path)
    else:
        return temp_pk
    
if __name__ == '__main__':
    
    pk = pd.read_excel('../raw_data/pk.xlsx')
    temp_pk = ExpandPk(pk, save=True, save_path='../temp_data/pk.xlsx')