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
                 '班组名称', '职员代码', '设备名称', '设备代码', '等级']
    temp_pk.drop(drop_list, axis=1, inplace=True)
    
    #删除异常的芯棒编码
    temp_pk = bf.Del(temp_pk, '芯棒编码')
    
    #删除平均值行，并把位置列转为数值类型
    temp_pk = temp_pk[temp_pk['位置'] != '平均值']
    temp_pk['位置'] = [int(x) for x in temp_pk['位置']]
    
    #把异常的位置归到附近的位置
    def Func(x):
        if 100 < x < 200:
            return 200
        elif 500 < x <700:
            return 700
        elif 350 < x < 400:
            return 400
        elif 300 < x < 350:
            return 300
        elif x > 700:
            return 700
        else:
            return x
    temp_pk['位置'] = [Func(x) for x in temp_pk['位置']]
  
    #把负的那一列转为位置
    temp_pk['新位置'] = [x['长度'] - x['位置'] if x['反面'] == 1 
                        else x['位置'] 
                        for loc, x in temp_pk.iterrows()]
    #添加归一化列
    def Func_1(df):
        df['归一化'] = [int(x) / int(df['长度'].max()) for x in df['新位置']]
        return df
    temp_pk = temp_pk.groupby('芯棒编码', sort=False, as_index=False).apply(Func_1)
    
    #给归一化后的数值加一个范围
    def Func_2(df):
        if 0 not in df['反面'].values:
            df_1 = df[df['反面'] == 1]
            df_1.sort_values('归一化', inplace=True)
            min_num_1 = list(df_1['归一化'].values)
            max_num_1 = list(df_1['归一化'].values[1:])
            max_num_1.append(1)
            df_1['min_num'] = min_num_1
            df_1['max_num'] = max_num_1
            df_1['zhong_min'] = 0
            df_1['zhong_max'] = df_1['归一化'].values[0]
            df_1['zhong_位置'] = df_1['新位置'].values[0] / 2
            return df_1
        
        elif 1 not in df['反面'].values:
            df_0 = df[df['反面'] == 0]
            df_0.sort_values('归一化', inplace=True)
            min_num_0 = list(df_0['归一化'].values[:-1])
            min_num_0.insert(0, 0)
            max_num_0 = list(df_0['归一化'].values)
            df_0['min_num'] = min_num_0
            df_0['max_num'] = max_num_0
            df_0['zhong_min'] = df_0['归一化'].values[-1]
            df_0['zhong_max'] = 1
            df_0['zhong_位置'] = (df_0['新位置'].values[-1] + df['长度'].values[0]) / 2
            return df_0
        
        else:
            df_0 = df[df['反面'] == 0]
            df_0.sort_values('归一化', inplace=True)
            min_num_0 = list(df_0['归一化'].values[:-1])
            min_num_0.insert(0, 0)
            max_num_0 = list(df_0['归一化'].values)
            df_0['min_num'] = min_num_0
            df_0['max_num'] = max_num_0
            
            df_1 = df[df['反面'] == 1]
            df_1.sort_values('归一化', inplace=True)
            min_num_1 = list(df_1['归一化'].values)
            max_num_1 = list(df_1['归一化'].values[1:])
            max_num_1.append(1)
            df_1['min_num'] = min_num_1
            df_1['max_num'] = max_num_1
            
            df = df_0.append(df_1)
            df['zhong_min'] = df_0['归一化'].values[-1]
            df['zhong_max'] = df_1['归一化'].values[0]
            df['zhong_位置'] = (df_0['新位置'].values[-1] + df_1['新位置'].values[0]) / 2
            return df
            
# =============================================================================
#         if 0 in df['反面'].values:
#             df_0 = df[df['反面'] == 0]
#             df_0.sort_values('归一化', inplace=True)
#             min_num_0 = list(df_0['归一化'].values)
#             max_num_0 = list(df_0['归一化'].values[1:])
#             max_num_0.append(1)
#             df_0['min_num'] = min_num_0
#             df_0['max_num'] = max_num_0
#             
#         if 1 not in df['反面'].values:
#             return df_0
#         elif 0 not in df['反面'].values:
#             return df_1
#         else:
#             df = df_0.append(df_1)
#             return df
# =============================================================================
    
    temp_pk = temp_pk.groupby('芯棒编码', sort=False, as_index=False).apply(Func_2)
    
    #重命名列名并删除相关列
    temp_pk = bf.Rename(temp_pk, prefixes='pk')
    temp_pk.drop(['pk_位置', 'pk_反面'], axis=1, inplace= True)
    
    #保存处理后的文件
    if save == True:
        bf.Save(temp_pk, save_path)
        return None
    else:
        return temp_pk
    
if __name__ == '__main__':
    
    pk = pd.read_excel('../raw_data/pk.xlsx')
    temp_pk = ExpandPk(pk, save=True, save_path='../temp_data/pk.xlsx')#, save=True, save_path='../temp_data/pk.xlsx'