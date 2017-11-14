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

def Merge(pk, core, ovd, fiber, related, save=None, save_path=None):
    
    #合并pk和core
    pk_core = pd.merge(core, pk, left_on='core_芯棒编码', right_on='pk_芯棒编码', how='inner')
    pk_core.drop('pk_芯棒编码', axis=1, inplace=True)
    
    #合并pk_core和ovd
    pk_core_ovd = pd.merge(ovd, pk_core, left_on='ovd_短芯棒编码', right_on='core_芯棒编码', how='inner')
    pk_core_ovd.drop('ovd_短芯棒编码', axis=1, inplace=True)
    
    #合并pk_core_ovd和related
    related.drop(['序号', '厂商', '入库日期'], axis=1, inplace=True)
    pk_core_ovd_related = pd.merge(related, pk_core_ovd, left_on='光棒编号', right_on='ovd_芯棒编码', how='inner')
    pk_core_ovd_related.drop('ovd_芯棒编码', axis=1, inplace=True)
    
    #合并pk_core_ovd_related和fiber
    final = pd.merge(fiber, pk_core_ovd_related, left_on='条码_光纤预制棒编号', right_on='光纤编号', how='inner')
    final.drop('光纤编号', axis=1, inplace=True)
    
    if save == True:
        bf.Save(final, save_path)
    else:
        return final
    
if __name__ == '__main__':
    
    pk = pd.read_excel('../temp_data/pk.xlsx')
    core = pd.read_excel('../temp_data/core.xlsx')
    ovd = pd.read_excel('../temp_data/ovd.xlsx')
    fiber = pd.read_excel('../temp_data/fiber.xlsx')
    related = pd.read_excel('../temp_data/光棒-光纤对应标号.xlsx')
    see = Merge(pk, core, ovd, fiber, related)