import requests as rq
import re
from bs4 import BeautifulSoup
import pandas as pd
import fitz
import time
import os
# FIELD_DICT = 

def pdf_handler(file_name):
    doc = fitz.open('pdfs/'+file_name)
    pdf_text = doc[0].get_text()
    pdf_list = pdf_text.split('\n')
    pcode = get_content(pdf_list, ['项目编号：','项目编号:','项目编号','编号'],'')
    pname = get_content(pdf_list, ['项目名称：','项目名称:','项目名称','名称'],'')
    win1 = get_content(pdf_list, ['第一中标候选人：','第一中标候选人:','第一中标候选人','第1中标候选人','成交候选人'],'公司')
    win2 = get_content(pdf_list, ['第二中标候选人：','第二中标候选人:','第二中标候选人','第2中标候选人'],'公司')
    if get_content(pdf_list,['标段一','标段二','标段三']) !='':
        hasbd = 1
    else:
        hasbd = 0

    line_data = (file_name,pcode,pname,win1,win2,hasbd)
    return line_data
    # print(pdf_text.find('\n'))
def get_content(line_list,travel_list,end_str = ''):
    for tra in travel_list:
        for line in line_list:
            pname = find_inline(line,tra,end_str)
            if pname != None:
                return pname
    return ''

def find_inline(line,start,end):
    start_index = line.find(start)

    if end == '':
        if start_index >=0:
            return line[start_index+len(start):]
    else:
        end_index = line.find(end)
        if start_index >=0 and end_index > 0:
            return line[start_index+len(start):end_index+len(end)]

if __name__ == '__main__':
    filelist = os.listdir('./pdfs')
    data_list = []
    for file in filelist:
        data_list.append(pdf_handler(file))
    df = pd.DataFrame(data_list,columns=['file_name', 'pcode','pname','win1','win2','hasbd'])
    df.to_csv('result.csv',encoding='utf-8')
# pdf_handler()