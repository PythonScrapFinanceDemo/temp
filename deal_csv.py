import pandas as pd
from pandas import Series,DataFrame
import numpy as np
import csv
import sys,os


def get_date(filename):
    date = filename.split('-')
    return date[1]+'-'+date[2]+'-'+date[3]

def rebuild_csv(folderName,label=0):
    '''
    如果 非前四组，令label=1
    '''
    files = []  #存储所有的csv文件名
    for (dirpath, dirnames, filenames) in os.walk(folderName):
        files.extend(filenames)
        break

    for file_i in range(len(files)):
        filename = files[file_i]
        if file_i == 0:
            temp_df = pd.read_csv(os.path.join(folderName,filename),encoding="gb18030")
            temp_df['时间'] = Series(get_date(filename),index=temp_df.index)
            temp_df['排行榜'] = Series(folderName,index=temp_df.index)
            if '组别' not in temp_df.columns:
                temp_df['组别'] = Series('-',index=temp_df.index)
            df = temp_df
        else:
            temp_df = pd.read_csv(os.path.join(folderName,filename),encoding="gb18030")
            temp_df['时间'] = Series(get_date(filename),index=temp_df.index)
            temp_df['排行榜'] = Series(folderName,index=temp_df.index)
            if '组别' not in temp_df.columns:
                temp_df['组别'] = Series('-',index=temp_df.index)
            df = df.append(temp_df,ignore_index=True)
    if label == 1:
        df['净利润得分'] = Series('-',index=temp_df.index)
        df['回撤率得分'] = Series('-',index=temp_df.index)
        df['净值得分'] = Series('-',index=temp_df.index)
        df['综合得分'] = Series('-',index=temp_df.index)
    df['客户代码'] = Series('-',index=temp_df.index) #先设置为‘-’，以后再判断
    df.to_csv(folderName+'.csv',index=False)

'''
temp codes:

temp.sort('排名', ascending=False)
'''


if __name__ == '__main__':
    #rebuild_csv('ChengXuHuaZu_1')
    rebuild_csv('Jijinzu')
    rebuild_csv('GuiJinShu_9月1号到9月30号',1)
