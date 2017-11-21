# -*- coding: utf-8 -*-
"""
Created on Tue Nov 21 15:49:10 2017

@author: Administrator
"""

'''
合并数据的版本_2
直接按照长度合并，不按照比例了
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
    
    #对pk_core_ovd_related的光棒编码进行筛选，去掉那些异常的
    pk_core_ovd_related = bf.Del(pk_core_ovd_related, '光棒编号')
    
    #删除位置为'平均值'的行
    pk_core_ovd_related = pk_core_ovd_related[pk_core_ovd_related['pk_位置'] != '平均值']
    pk_core_ovd_related['pk_位置'] = [int(x) for x in pk_core_ovd_related['pk_位置']]
    
    #把表按照正反面展开
#    temp = [x for x in see.columns if see[x].dtype == 'O']
#    temp_data = pk_core_ovd_related[temp].drop_duplicates()
#    pk_core_ovd_related_la = pk_core_ovd_related.pivot_table(index='光棒编号', columns='pk_反面')
#    pk_core_ovd_related_la
    
# =============================================================================
#     #按照说明要求把光棒编码进行拆分
#     split_dict = {'光纤类型': [0], 'VAD塔线': [1], '四位流水码': [2,5], 'VAD烧结塔线': [6],
#                   '拉伸塔线': [7], '分棒编号': [8], 'OVD塔线': [9], 'OVD左、右、中间轴': [10]}
#     pk_core_ovd_related = bf.SplitNumber(pk_core_ovd_related, '光棒编号', split_dict=split_dict)
# =============================================================================
    
    #给pk的位置新增一列，找到其在光棒中的位置
    
    return pk_core_ovd_related

if __name__ == '__main__':
    
    pk = pd.read_excel('../temp_data/pk.xlsx')
    core = pd.read_excel('../temp_data/core.xlsx')
    ovd = pd.read_excel('../temp_data/ovd.xlsx')
    fiber = pd.read_excel('../temp_data/fiber.xlsx')
    related = pd.read_excel('../temp_data/光棒-光纤对应标号.xlsx')
    see = Merge(pk, core, ovd, fiber, related)