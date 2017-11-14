# -*- coding: utf-8 -*-
"""
Created on Tue Nov 14 20:51:22 2017

@author: Administrator
"""

'''
处理core
'''
import pandas as pd
import basic_func as bf

def Core(data, save=None, save_path=None):
    
    temp_data = data.copy()
    
    #删除不必要的列
    drop_list = ['单据编号', '状态', '芯棒类型', '测试人', '测试日期',
                 '班组', '设备', '异常原因', '备注', '建单人', '建单日期']
    temp_data.drop(drop_list, axis=1, inplace=True)
    
    #更换列名
    temp_data = bf.Rename(temp_data, prefixes='core')
    
    #保存处理后的文件
    if save == True:
        bf.Save(temp_data, save_path)
    else:
        return temp_data

if __name__ == '__main__':
    
    core = pd.read_excel('../raw_data/core rod runout.xlsx')
    temp_core = Core(core, save=True, save_path='../temp_data/core.xlsx')