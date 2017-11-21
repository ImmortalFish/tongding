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
# =============================================================================
#     #把平均值换成数值
#     def Func(df):
#         df['新位置'] = df['位置']
#         if '平均值' in df['位置'].values:
#             mean_num = int(df['位置'][:-1].astype('int').mean())
#             df['新位置'].replace('平均值', mean_num, inplace=True)
#             df['新位置'] = df['新位置'].astype('int')
#         return df
#     temp_pk = temp_pk.groupby('芯棒编码', sort=False, as_index=False).apply(Func)
# =============================================================================
  
    #把负的那一列转为位置
    temp_pk['新位置'] = [x['长度'] - x['位置'] if x['反面'] == 0 
                        else x['位置'] 
                        for loc, x in temp_pk.iterrows()]
    #添加归一化列
    def Func_1(df):
        df['归一化'] = [int(x) / int(df['长度'].max()) for x in df['新位置']]
        return df
    temp_pk = temp_pk.groupby('芯棒编码', sort=False, as_index=False).apply(Func_1)
    
    #给归一化后的数值加一个范围
    
    
# =============================================================================
#     #给归一化后的数值一个范围
#     def Func_2(df):
#         df.sort_values('归一化', inplace=True)
#         drop_values = df['归一化'].drop_duplicates().values
#         range_list = []
#         range_list.append('0,' + str(drop_values[0]))
#         for i in range(len(drop_values)):
#             if i + 1 < len(drop_values):
#                 range_list.append(str(drop_values[i]) + ',' + str(drop_values[i + 1]))
#         range_list.append(str(drop_values[-1]) + ',1')
#         
#         add_list = []
#         for x in df['归一化'].values:
#             for j in range(len(range_list)):
#                 if float(range_list[j].split(',')[0]) < x <= float(range_list[j].split(',')[1]):
#                     add_list.append(range_list[j])
#                     continue
#         df['归一化范围'] = add_list
#         return df
#     temp_pk = temp_pk.groupby('芯棒编码', sort=False, as_index=False).apply(Func_2)
# =============================================================================
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
    temp_pk = ExpandPk(pk)#, save=True, save_path='../temp_data/pk.xlsx'