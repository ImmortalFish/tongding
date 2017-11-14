# -*- coding: utf-8 -*-
"""
Created on Tue Nov 14 21:05:30 2017

@author: Administrator
"""

'''
处理ovd
'''
import pandas as pd
import basic_func as bf

def Ovd(data, save=None, save_path=None):
    
    temp_data = data.copy()
    temp_data.dropna(axis=0, how='all', inplace=True)
    
    #删除不必要的列
    drop_list = ['单据编号', '状态', '测试人', '测试日期', '班组', '备注', '建单人', '建单日期']
    temp_data.drop(drop_list, axis=1, inplace=True)
    
    #把芯棒编码分成两部分
    temp_data['短芯棒编码'] = [x[:-1] if len(x) == 10 else x[:-2] for x in temp_data['芯棒编码']]
    
    #更换列名
    temp_data = bf.Rename(temp_data, prefixes='ovd')
    
    #保存处理后的文件
    if save == True:
        bf.Save(temp_data, save_path)
    else:
        return temp_data
    
if __name__ == '__main__':
    
    ovd = pd.read_excel('../raw_data/OVD soot data.xlsx')
    temp_ovd = Ovd(ovd, save=True, save_path='../temp_data/ovd.xlsx')