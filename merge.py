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
    
    #对pk_core_ovd_related的光棒编码进行筛选，去掉那些异常的
    pk_core_ovd_related = bf.Del(pk_core_ovd_related, '光棒编号')
    
    #按照说明要求把光棒编码进行拆分
    split_dict = {'光纤类型': [0], 'VAD塔线': [1], '四位流水码': [2,5], 'VAD烧结塔线': [6],
                  '拉伸塔线': [7], '分棒编号': [8], 'OVD塔线': [9], 'OVD左、右、中间轴': [10]}
    pk_core_ovd_related = bf.SplitNumber(pk_core_ovd_related, '光棒编号', split_dict=split_dict)
    
#    #通过反面展开pk
#    temp_frame = pk_core_ovd_related[['光棒编号', '光纤编号', 'ovd_设备', 'core_芯棒编码', 'core_等级', 'pk_位置',
#                'pk_等级', 'pk_设备代码', 'pk_归一化', '光棒编号_光纤类型', '光棒编号_VAD塔线',
#                '光棒编号_四位流水码', '光棒编号_VAD烧结塔线', '光棒编号_拉伸塔线', '光棒编号_分棒编号',
#                '光棒编号_OVD塔线', '光棒编号_OVD左、右、中间轴']].drop_duplicates()
#    
#    pk_core_ovd_related = pk_core_ovd_related.pivot_table(index='光棒编号', columns='pk_反面')
#    pk_core_ovd_related.reset_index(inplace=True)
#    
#    pk_core_ovd_related = bf.Rename1(pk_core_ovd_related)
#    pk_core_ovd_related = pd.merge(temp_frame, pk_core_ovd_related, on='光棒编号')
    
    #给pk归一化一个范围
    def Func(df):
        df.sort_values('pk_归一化', inplace=True)
        drop_values = df['pk_归一化'].drop_duplicates().values
        range_list = []
        range_list.append([0, drop_values[0]])
        for i in range(len(drop_values)):
            if i+1 < len(drop_values):
                range_list.append([drop_values[i], drop_values[i + 1]])
        range_list.append([drop_values[-1], 1])
        
        add_list = []
        for x in df['pk_归一化'].values:
            for j in range(len(range_list)):
                if range_list[j][0] < x <= range_list[j][-1]:
                    add_list.append(range_list[j])
                    continue
        df['pk_归一化范围'] = add_list
        return df
    pk_core_ovd_related = pk_core_ovd_related.groupby('光棒编号', sort=False, as_index=False).apply(Func)
        
    #合并pk_core_ovd_related和fiber
    final = pd.merge(fiber, pk_core_ovd_related, left_on='条码_光纤预制棒编号', right_on='光纤编号', how='inner')
    final.drop('光纤编号', axis=1, inplace=True)
    
    def Func_1(df):
        temp_fiber = df['归一化'].drop_duplicates().values
        add_list = []
        for i in df['pk_归一化范围']:
            if i[0] < temp_fiber <= i[-1]:
                add_list.append(i)
            else:
                add_list.append(0)
        df['new_范围'] = add_list
        return df
    final = final.groupby('条码', sort=False, as_index=False).apply(Func_1)
    final = final[final['new_范围'] != 0]
    
    #删除不必要的列
    drop_list = ['等级', '计划物料编码', '实际物料编码', '生产日期', '检验日期', '备注', '归一化', 
                 'ovd_设备', 'pk_设备代码', 'core_芯棒编码', 'pk_归一化范围', 'pk_归一化', 'new_范围']
    final.drop(drop_list, axis=1, inplace=True)
    
    #通过反面展开fiber
#    fiber_name = list(final.columns)[:58]
#    final.pivot_table(index='条码', columns='反面', values=[])
    
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
    see = Merge(pk, core, ovd, fiber, related, save=True, save_path='../final_data/final_not_laping.xlsx')