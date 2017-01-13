# coding:utf-8
from bs4 import BeautifulSoup
import requests
import postpacketpayload as GetPostPacket

#给一个日期，返回该日期对应的第一个页面的html代码
def getOneDayFirstPage(Date):
    url = "http://spds.qhrb.com.cn/SP10/SPOverSee1.aspx"
    WantedPage =1
    payload = GetPostPacket.getQingLiangZuPayload(WantedPage,Date)
    headers = GetPostPacket.getQingLiangZuHeaders()

    response = requests.request("POST", url, data=payload, headers=headers)

    return response.text


#给一个日期，返回该日期对应的所有页面数量
def getOneDayTotalPageNumber(Date):
    source_code = getOneDayFirstPage(Date)
    plain_text=str(source_code)
    bsObj = BeautifulSoup(plain_text,'html.parser')
    #因为page在不同组或者不同日下会有变化，每次获取某日某组所有日之前需要获取最新的页数
    #bsObj = BeautifulSoup(driver.page_source,'html.parser')
    page_option = bsObj.find('select',id="AspNetPager1_input").findAll('option')
    page_length = int(page_option[len(page_option)-1].get_text())    #获得所有页数

    return page_length

if __name__ == "__main__":
    Date = "2016-04-06"
    totalPageNumber = getOneDayTotalPageNumber(Date)
    print totalPageNumber