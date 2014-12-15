#!/usr/bin/env python
# coding: utf-8
from StringIO import StringIO
import re
import json
import requests
import datetime
import pandas as pd
import prettytable 

headers = {
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encoding":"gzip, deflate",
    "Accept-Language":"zh-TW,zh;q=0.8,en-US;q=0.6,en;q=0.4,zh-CN;q=0.2",
    "Cache-Control":"no-cache",
    "Connection":"keep-alive",
    "Content-Length":"656",
    "Content-Type":"application/x-www-form-urlencoded",
    "DNT":"1",
    "Host":"dengue.kcg.gov.tw",
    "Origin:http":"//dengue.kcg.gov.tw",
    "Pragma":"no-cache",
    "Referer:http":"//dengue.kcg.gov.tw/KCGDengue/Mobile.aspx",
    "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.65 Safari/537.36"
        }

data = {
    "__EVENTTARGET":"Button_Search",
    "__EVENTARGUMENT":"",
    "__VIEWSTATE":"/wEPDwULLTEwMDAwMTExMjkPZBYCAgMPZBYCAgkPD2QWAh4Hb25jbGljawVCdGhpcy5kaXNhYmxlZD10cnVlO1Nob3dMb2FkaW5nKCk7X19kb1Bvc3RCYWNrKCdCdXR0b25fU2VhcmNoJywnJyk7ZGSLHYBiGA1yiwZ2u7zJ63cbRA2vm5fq+hbYFNAMVjOx1Q==",
    "__VIEWSTATEGENERATOR":"413B2934",
    "__EVENTVALIDATION":"/wEdAAgWGG2RY7jiUVmjHVLA3Vuhehn3bx2onw+gsGVGxW2uqPNH0QUya0tFKkgIABYfTinPqMgpP5oNyRNOFC9UkRd5TOB3/nlg9WQl65G7nSsW3XNGFTzwHLRD2v/eJGCd0ynBitcvyf0ePx5gnv8TklictmXUWyWAGbecBNn3zDP8oVEqyvt2y+R5rbK1ebIZhW17xDILuWgEcbUxmBSNbL8K",
    "DropDownList_CaseType":"Confirm",  #DHF Confirm
    "DropDownList_AreaType":"DIST", #DIST VILLAGE
        }

date = datetime.date(2014,12,10)
F = {}
for i in range(5):
        data["TextBox_Start"] = date
        date += datetime.timedelta(days=1)
        data['TextBox_End'] = date
        print data['TextBox_Start'] , data['TextBox_End']

        html = requests.post('http://dengue.kcg.gov.tw/KCGDengue/Mobile.aspx', verify=False, headers=headers, data=data)
        match = re.findall(u'var AREA =  new Array\((.*?)\);', html.text)
        match2 = re.findall(u'var NUMB =  new Array\((.*?)\);', html.text)
        if match == [] : continue 
        Area = [x.strip("'") for x in match[0].split(', ')]
        Count = [ int(x) for x in match2[0].split(', ')]
        final = dict(zip(Area, Count))
        F[date.strftime('%Y-%m-%d')] = final
        F.update(F)        
        
df = pd.DataFrame.from_dict(F, orient='columns')
newset = df.T.fillna(0)
output = StringIO()
newset.to_csv(output,encoding='utf-8',sep=',')
output.seek(0)
print prettytable.from_csv(output)
