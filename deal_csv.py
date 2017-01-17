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
        temp_df = pd.read_csv(os.path.join(folderName,filename),encoding="gb18030")
        temp_df['时间'] = Series(get_date(filename),index=temp_df.index)
        temp_df['排行榜'] = Series(folderName,index=temp_df.index)
        if '组别' not in temp_df.columns:
            temp_df['组别'] = Series('-',index=temp_df.index)
        if file_i == 0:
            df = temp_df
        else:
            df = df.append(temp_df,ignore_index=True)
    if label == 1:
        df['净利润得分'] = Series('-',index=temp_df.index)
        df['回撤率得分'] = Series('-',index=temp_df.index)
        df['净值得分'] = Series('-',index=temp_df.index)
        df['综合得分'] = Series('-',index=temp_df.index)
    df['客户代码'] = Series('-',index=temp_df.index) #先设置为‘-’，以后再判断
    cols = df.columns.tolist()
    cols.sort()
    df = df[cols]
    df.to_csv(folderName+'.csv',index=False)

def all_to_one(nameList):
    for df_i in range(len(nameList)):
        df_name = nameList[df_i]+'.csv'
        temp_df = pd.read_csv(df_name, low_memory=False)
        if df_i == 0:
            total_df = temp_df
        else:
            total_df = total_df.append(temp_df,ignore_index=True)
    total_df.to_csv('total_temp.csv')
    return total_df

def deal_csv(folderName,label=0):
    filetowrite=open(folderName+'.csv','a')
    writer=csv.writer(filetowrite)

    files = []  #存储所有的csv文件名
    for (dirpath, dirnames, filenames) in os.walk(folderName):
        files.extend(filenames)
        break

    for file_i in range(len(files)):
        filename = files[file_i]
        temp_df = pd.read_csv(os.path.join(folderName,filename),encoding="gb18030")
        temp_df['时间'] = Series(get_date(filename),index=temp_df.index)
        temp_df['排行榜'] = Series(folderName,index=temp_df.index)
        if '组别' not in temp_df.columns:
            temp_df['组别'] = Series('-',index=temp_df.index)
        if label == 1:
            temp_df['净利润得分'] = Series('-',index=temp_df.index)
            temp_df['回撤率得分'] = Series('-',index=temp_df.index)
            temp_df['净值得分'] = Series('-',index=temp_df.index)
            temp_df['综合得分'] = Series('-',index=temp_df.index)
        temp_df['客户代码'] = Series('-',index=temp_df.index) #先设置为‘-’，以后再判断
        cols = temp_df.columns.tolist()
        cols.sort()
        temp_df = temp_df[cols]
        temp_df.to_csv('temp_df.csv')
        filetoread=open('temp_df.csv','r')
        reader=csv.reader(filetoread)
        if file_i != 0:
            for i,line in enumerate(reader):
                if i != 0:
                    writer.writerow(line)
        else:
            for line in reader:
                writer.writerow(line)
        print(file_i)
    filetowrite.close()

def chenge_columns_order(columns_list):
    temp_df = pd.read_csv('total_temp.csv', low_memory=False)
    temp_df = temp_df[columns_list]
    temp_df.to_csv('total_temp_nc.csv')

def sort_df():
    temp_df = pd.read_csv('total_temp_nc.csv', low_memory=False)
    temp_df = temp_df.sort_values(['客户昵称','排名'], ascending=[True,True])
    temp_df.to_csv('total_temp_new.csv')


def get_id():
    pass

if __name__ == '__main__':
    '''
    deal_csv('JiJinZu')
    deal_csv('ChengXuHuaZu')
    deal_csv('QingLiangZu')
    deal_csv('ZhongLiangZu')
    deal_csv('GuiJinShu',1)
    deal_csv('NongChanPin',1)
    deal_csv('NengYuanHuaGong',1)
    deal_csv('YouSeJinShu',1)
    deal_csv('JinRongQiHou',1)
    deal_csv('JingLiRun',1)
    all_to_one(['JiJinZu','ChengXuHuaZu','QingLiangZu','ZhongLiangZu','GuiJinShu','NongChanPin','NengYuanHuaGong','YouSeJinShu','JinRongQiHou','JingLiRun'])

    columns_list = ['客户昵称','组别','排行榜','时间','排名','当日权益','风险度(%)','净利润','净利润得分','回撤率(%)','回撤率得分','日净值','累计净值',
                    '净值得分','综合得分','参考收益率(%)','指定交易商','操作指导','账户评估']

    chenge_columns_order(columns_list)
    '''
    sort_df()
