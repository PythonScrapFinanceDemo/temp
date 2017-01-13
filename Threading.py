# -*- coding: UTF-8 -*-
import requests
import Queue
import threading
import time
import date as date_list
import pagenumber as GetTotalPageNumber
import postpacketpayload as GetPostPacket
import write as WriteInCSV

class myThread (threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
    def run(self):
        print "Starting " + self.name + "\n"
        process_data(self.name)
        print "Exiting " + self.name + "\n"
def process_data(threadName):
        data = str(threadName.split('-')[1])
        print "%s processing %s的%s页\n" % (threadName,Date, data)
        url = "http://spds.qhrb.com.cn/SP10/SPOverSee1.aspx"
        #要加上一个参数用来判断哪一组，还待完善
        payload = GetPostPacket.getQingLiangZuPayload(data,Date)
        headers = GetPostPacket.getQingLiangZuHeaders()
        response = requests.request("POST", url, data=payload, headers=headers)
        page_source = response.text
        result_successfully = WriteInCSV.select_data(page_source)
        print "存储"+Date +"的"+ str(data) + "页中的数据\n"
        print result_successfully

        time.sleep(0)


if __name__ == "__main__":
    total_start =time.clock()
    Datelist = date_list.get_date_list('2016-04-01','2016-05-01')
    for Date in Datelist:
        TotalPageNmber = GetTotalPageNumber.getOneDayTotalPageNumber(Date)
        nameList = [i for i in  range(1,int(TotalPageNmber)+1)]
        threadList  = ["thread-" + str(n) for n in nameList]
        threadID = 1
        # 创建新线程
        for tName in threadList:
            thread = myThread(threadID, tName)
            #启动线程
            thread.start()
            threadID += 1

    total_end = time.clock()
    print 'whole project Running time: %s Seconds\n'%(total_end-total_start)
