# -*- coding: utf-8 -*-
"""
Created on Sun Nov 12 21:04:37 2017

@author: Administrator
"""

'''
拆分说明中的那些编号
'''

import pandas as pd
pd.options.mode.chained_assignment = None

class table(object):
    
    def __init__(self, data, name):
        self.data = data
        self.data.dropna(axis=0, how='all', inplace=True)
        self.data.dropna(axis=1, how='all', inplace=True)
        self.name = name
    
    def Del(self, len_list=(5,7,8), inplace=None):
        '''删除那些异常的编码'''
        temp_data = self.data.copy()
        col_name = self.name
        temp_data['judge'] = [True if len(x) in len_list else False for x in temp_data[col_name]]
        temp_data = temp_data[temp_data['judge'] == False]
        temp_data.drop('judge', axis=1, inplace=True)
        
        if inplace == True:
            self.data = temp_data
        else:
            return temp_data
    
    def SplitNumber(self, split_dict=None, inplace=None):
        '''拆分编码'''
        temp_data = self.data.copy()
        for key, value in split_dict.items():
            name = self.name + '_' + key
            temp_data[name] = temp_data[self.name].apply(lambda x: x[value[0] : value[-1] + 1])
        
        if inplace == True:
            self.data = temp_data
        else:
            return temp_data
    
    def AddNormalized(self, length_name, inplace=None):
        '''增加长度的归一化'''
        name = length_name + '_' + '归一化'
        len_max = self.data[length_name].max()
        len_min = self.data[length_name].min()
        self.data[name] = self.data[length_name].apply(lambda x: (x - len_min) / (len_max - len_min))
    
    
if __name__ == '__main__':
    
    path = '../raw_data/OVD soot data.xlsx'
    data = pd.read_excel(path)
    name = '芯棒编码'
    split_dict = {'xinbang_11': {'光纤类型':[0], 'VAD塔线':[1], '流水码':[2,5], 'VAD烧结塔线':[6], '拉伸塔线':[7], '分棒编号':[8], 'OVD塔线':[9], 'OVD左右中间轴':[10]},
                  'xinbang_9': {'光纤类型':[0], 'VAD塔线':[1], '流水码':[2,5], 'VAD烧结塔线':[6], '拉伸塔线':[7], '分棒编号':[8]},
                  'xiaopan': {'拉丝塔号': [0,2], '光纤预制棒编号': [3,16], '大小盘': [17,19]}}
    
    new_table = table(data, '芯棒编码')
    data = new_table.data
    new_table.Del(inplace=True)
    data_split = new_table.SplitNumber(split_dict['xinbang_11'], inplace=False)