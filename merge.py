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
        
    #合并pk_core_ovd_related和fiber
    final = pd.merge(fiber, pk_core_ovd_related, left_on='条码_光纤预制棒编号', right_on='光纤编号', how='left')
    final.drop('光纤编号', axis=1, inplace=True)
    
    #为fiber表的归一化定义一个flag来指示是否在这个区间里
    final['flag'] = [1 if x['pk_min_num'] < x['归一化'] <= x['pk_max_num'] else -1 if x['pk_zhong_min'] < x['归一化'] < x['pk_zhong_max'] else 0 for index, x in final.iterrows()]
    
    
    final = final[final['flag'] != 0]
    final['pk_新位置'] = [x['pk_zhong_位置'] if x['flag'] == -1 else x['pk_新位置'] for index, x in final.iterrows()]
    final = final.groupby('条码', sort=False, as_index=False).apply(lambda x: x.iloc[:1,:])
    
    #删除不必要的列
    drop_list = ['等级', '计划物料编码', '实际物料编码', '生产日期', '检验日期', '备注', '归一化', 
                 'ovd_设备', 'core_芯棒编码', 'pk_归一化', 'pk_min_num', 'pk_max_num',
                 'pk_zhong_min', 'pk_zhong_max', 'pk_zhong_位置']
    final.drop(drop_list, axis=1, inplace=True)
    
    if save == True:
        bf.Save(final, save_path)
        return None
    else:
        return final
    
if __name__ == '__main__':
    
    pk = pd.read_excel('../temp_data/pk.xlsx')
    core = pd.read_excel('../temp_data/core.xlsx')
    ovd = pd.read_excel('../temp_data/ovd.xlsx')
    fiber = pd.read_excel('../temp_data/fiber.xlsx')
    related = pd.read_excel('../temp_data/光棒-光纤对应标号.xlsx')
    see = Merge(pk, core, ovd, fiber, related, save=True, save_path='../final_data/final_11_21.xlsx')#, save=True, save_path='../final_data/final_11_21.xlsx'
     