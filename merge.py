# -*- coding: utf-8 -*-
"""
Created on Tue Nov 14 20:12:45 2017

@author: Administrator
"""

'''
合并大表
'''

import pandas as pd
import basic_func as bf

def Merge(*data, save=None, save_path=None):
    
    data_list = [x for x in data]
    
if __name__ == '__main__':
    
    pk = pd.read_excel('../temp_data/pk.xlsx')
    core = pd.read_excel('../temp_data/core rod runout.xlsx')
    ovd = pd.read_excel('../temp_data/OVD soot data.xlsx')
    fiber = pd.read_excel('../temp_data/fiber data.xlsx')
    related = pd.read_excel('../temp_data/光棒-光纤对应标号.xlsx')