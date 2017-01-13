from urllib.request import urlopen
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import pandas as pd
import numpy as np

#清洗掉数据中的垃圾，该函数只针对columns_text，看起来是个失败
def get_plain_text(ResultSet):
    text = []
    for i in ResultSet:
        text.append(i.get_text().split()[0])    #因为split()返回的是字符串列表，所以要加[0]
    return text

#读取数据，提取并清洗数据，最后装入user_information中
def select_data(driver):
    user_information = []
    bsObj = BeautifulSoup(driver.page_source,'html.parser')
    try:
        user_information_obj = bsObj.findAll('tr',style="background: #fff;")
    except Exception as e:
        print("No datas")
    else:
        for i,user_i in enumerate(user_information_obj):
            temp = []
            for td_i in user_i.findAll("td"):
                temp_data = td_i.get_text().split()
                if not temp_data:     #无数据
                    temp.append("-")
                else:
                    temp.append(temp_data[0])
            user_information.append(temp)

        columns = bsObj.findAll(style="padding-top: 1px;")
        columns_text = get_plain_text(columns)
        columns_text.insert(0,'排名')

        page_now = int(bsObj.find('select',id="AspNetPager1_input").find('option',selected="true").get_text())

        df = pd.DataFrame(user_information,columns = columns_text) #使用pandas储存数据
        df.to_csv(group_name[group_i]+'-'+date+'-'page_now+'.csv',index=False) #每采集完一日的一组后，存储一次
