# -*- coding: utf-8 -*-
"""
Created on Mon Nov 13 15:30:01 2017

@author: Administrator
"""

'''
重命名数据集列名
'''


class renamedata(object):
    
    def __init__(self, data):
        self.data = data
    
    def Rename(self, prefixes=None, inplace=None, save=None, save_path=None):
        temp_data = self.data.copy()
        if prefixes is None:
            prefixes = ''
        else:
            prefixes = prefixes +'_'
        
        new_name = map(lambda x: prefixes + x, list(temp_data.columns))
        temp_data.columns = new_name
        
        if inplace == True:
            self.data = temp_data
        else:
            return temp_data
            
        if save == True:
            try:
                temp_data.to_excel(save_path)
            except Exception as e:
                print('save_path throw a error!', e)
        else:
            pass
    
#        
#if __name__ == '__main__':
#    
#    import pandas as pd
#    path = '../raw_data/pk.xlsx'
#    data = pd.read_excel(path)
#    new_rename = renamedata(data)
#    new = new_rename.Rename(prefixes='pk', inplace=False)
    