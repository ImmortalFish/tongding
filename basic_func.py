# -*- coding: utf-8 -*-
"""
Created on Mon Nov 13 11:12:17 2017

@author: Administrator
"""
'''
一些基本的函数
'''

import pandas as pd
pd.options.mode.chained_assignment = None

def Rename(data, prefixes=None):
    '''根据给定前缀prefixes重命名数据集的列名'''
    temp_data = data.copy()
    if prefixes is None:
        prefixes = ''
    else:
        prefixes = prefixes +'_'
    
    new_name = map(lambda x: prefixes + x, list(temp_data.columns))
    temp_data.columns = new_name
    
    return temp_data

def Rename1(data):
    '''重命名列名'''
    temp_data = data.copy()
    new_name = [str(x).strip(')').strip('(').replace("'", '').replace(', ', '-') for x in list(temp_data.columns)]
    new_name[0].strip('_')
    temp_data.columns = new_name
    return temp_data

def Save(data, save_path, file_type='excel'):
    '''保存文件'''
    if file_type == 'excel':
        data.to_excel(save_path, index=False, encoding='UTF-8')
    elif file_type == 'csv':
        data.to_csv(save_path, index=False, encoding='UTF-8')
    print('保存成功!')
    
def Del(data, name, len_list=(5,7,8)):
    '''删除给定数据集data中name属性列的异常的编码'''
    temp_data = data.copy()
    col_name = name
    temp_data['judge'] = [True if len(x) in len_list else False for x in temp_data[col_name]]
    temp_data = temp_data[temp_data['judge'] == False]
    temp_data.drop('judge', axis=1, inplace=True)

    return temp_data
    
def SplitNumber(data, name, split_dict=None):
    '''对给定数据集data的name属性列，按照说明拆分编码'''
    temp_data = data.copy()
    for key, value in split_dict.items():
        col_name = name + '_' + key
        temp_data[col_name] = temp_data[name].apply(lambda x: x[value[0] : value[-1] + 1])
    return temp_data
    
def AppendPk(pk_1, pk_2, save=None, save_path=None):
    '''合并pk_1和ok_2'''
    pk = pk_1.append(pk_2, ignore_index=True)
    if save == True:
        try:
            pk.to_excel(save_path, index=False, encoding='UTF-8')
        except Exception as e:
            print('save pk throw a error!', e)
    else:
        return pk
            
def MergeData(data_1, data_2, left_on, right_on, how='left', save=None, save_path=None):
    '''合并data_1和data_2两个表'''
    temp_merge = pd.merge(data_1, data_2, left_on=left_on, right_on=right_on, how=how)
    if save == True:
        try:
            temp_merge.to_excel(save_path, index=False, encoding='UTF-8')
        except Exception as e:
            print('save data throw a error!', e)
    else:
        return temp_merge
            
def Normalized(data, name, inplace=None):
    '''对给定数据集data的name列进行归一化'''
    temp_data = data.copy()
    new_col_name = name + '_' + '归一化'
    max_num = data[name].max()
    min_num = data[name].min()
    temp_data[new_col_name] = [(x - min_num) / (max_num - min_num) for x in temp_data[name]]
    
    if inplace == True:
        data = temp_data
    else:
        return temp_data
    
def LowerToUpper(data, name):
    '''对给定数据集data的name列进行小写转大写'''
    temp_data = data.copy()
    temp_data[name] = temp_data[name].apply(lambda x: x.upper())
    return temp_data