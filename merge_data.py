# -*- coding: utf-8 -*-
"""
Created on Sun Nov 12 18:51:03 2017

@author: Administrator
"""

'''
合并大表
'''

import pandas as pd

class mergedata(object):
    
    def __init__(self):
        pass
    
    def AppendPk(self, pk_1, pk_2, save=None, save_path=None):
        pk = pk_1.append(pk_2, ignore_index=True)
        if save == True:
            try:
                pk.to_excel(save_path, index=False, encoding='UTF-8')
            except Exception as e:
                print('save pk throw a error!', e)
    
    def MergeAll(self, *data, on=None, save=False, save_path=None):
        data_list = [x for x in data]
        temp_merge = data_list[0]
        for i in range(1, len(data_list)):
            temp_merge = pd.merge(temp_merge, data_list[i], how='left', on=on[i])
            
        

if __name__ == '__main__':
    
    path_1 = '../raw_data/pk.xlsx'
    path_2 = '../raw_data/core rod runout.xlsx'
    data_1 = pd.read_excel(path_1)
    data_2 = pd.read_excel(path_2)
    new = mergedata()
    a_list = new.MergeAll(data_1, data_2)