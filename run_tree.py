# -*- coding: utf-8 -*-
"""
Created on Thu Nov 16 10:29:10 2017

@author: Administrator
"""

'''
回归树模型
'''

import pandas as pd
from sklearn import tree

def Train(data, target_label, target_feature):
    '''训练回归树'''
    temp_data = data.copy()
    
    #删除一些不用的列
    drop_list = ['条码', '条码_拉丝塔号', '条码_光纤预制棒编号', '条码_大盘',
                 '条码_小盘', '光棒编号']
    temp_data.drop(drop_list, axis=1, inplace=True)
    
    #缺失值填充
    temp_data.fillna(0, inplace=True)
    
    #标签
    label = temp_data[target_label]
    
    #训练集
    train = temp_data[target_feature]
    
    #训练回归树
    clf = tree.DecisionTreeRegressor(max_depth=6, min_samples_leaf=10)
    clf.fit(train, label)
    f = tree.export_graphviz(clf, out_file=None, feature_names=target_feature)
    return f
    
if __name__ == '__main__':
    
    final = pd.read_excel('../final_data/final_laping.xlsx')
    target_label = '1310MFD'
    target_feature = ['ovd_有效长度-0', 'ovd_密度-0', 'ovd_重量-0']
    dot = Train(final, target_label, target_feature)