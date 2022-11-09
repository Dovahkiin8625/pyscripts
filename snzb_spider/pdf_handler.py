import requests as rq
import re
from bs4 import BeautifulSoup
import pandas as pd
import fitz
import time
# 3 获取字段


def get_field_data():
    df = pd.read_csv('urls_pdf.csv',encoding='utf-8')
    i = 0
    for d in df['url_pdf'][8:]:
        
        id = get_id(d)
        url = r'http://snzb.minegoods.com/sdnydzzb/cgUploadController.do?openFileById&id='+id
        # print(url)
        pdf_saver(url,id,5,i)
        i=i+1
def get_id(url_str):
    str_start = url_str.find(r"%26id%3D")+8
    str_end = url_str.find(r"&page=")
    return url_str[str_start:str_end]

def pdf_saver(url,id,retry_times,i):
    try:
        data_rq = rq.get(url)
        if data_rq.status_code!=200 or len(data_rq.content)<=0:
            raise Exception
        # print(data_rq.content)
        with open('pdfs/'+id+'.pdf','wb') as p:   
            p.write(data_rq.content) 
    except Exception as e:
        print("Save pdf failed,url = "+url)
        print("error = "+str(e))
        if retry_times>0:
            print("Retry after 5 seconds...")
            time.sleep(5)
            pdf_saver(url,id,retry_times-1,i)
        else:
            print("Skip this file")
    else:
        print("Save pdf succeeded, file_id: "+id+", i= "+str(i))

def pdf_handler():
    doc = fitz.open('t.pdf')
    print(doc[0].get_text())



# pdf_saver(TEST_URL,'id',2)
get_field_data()