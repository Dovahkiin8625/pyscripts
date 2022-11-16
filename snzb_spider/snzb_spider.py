import requests as rq
import re
from bs4 import BeautifulSoup
import pandas as pd
# 1 获取目录，1-240页所有文章的地址
# 99 1790
def save_dir_prefix():
    DIR_PREFIX_URL = r"http://snzb.minegoods.com/sdnycms/category/bulletinList.html?searchDate=1997-11-07&dates=300&word=&categoryId=10&tabName=%E4%B8%AD%E6%A0%87%E5%80%99%E9%80%89%E5%85%AC%E7%A4%BA&industryName=&status=&page="
    MAX_INDEX = 240 # 页码
    # 生成爬取的分页地址
    dir_url4re_list = []
    for i in range(MAX_INDEX):
        dir_url4re_list.append(DIR_PREFIX_URL +str(i+1))
    # print(dir_url4re_list)
    dir_prefix_urls = []
    for i in range(MAX_INDEX):
        url4re = DIR_PREFIX_URL +str(i+1)
        dir_prefix_rq = rq.get(url4re)
        dir_prefix_soup = BeautifulSoup(dir_prefix_rq.text,features="lxml")
        dir_prefix_list = dir_prefix_soup.select('body > div.container > div.zhaobiaoBox.relative > div:nth-child(2) > ul > li > a')
        print("add href from page:"+str(i))
        for li in dir_prefix_list:
            dir_prefix_urls.append(li['href'])

    df = pd.DataFrame(dir_prefix_urls,columns=['url'])
    df['url_pdf'] = ''
    print(df)
    df.to_csv('urls.csv',encoding='utf-8')

# 2 获取对应文章的pdf地址
'''
 * get_list: 指定从file_from中读取指定索引的url,如果为空，则读取所有
 * file_from: 读取所有文章地址的url文件
 * fiel_to: 获取的pdf地址的csv文件
'''
def get_pdf_url(get_list, file_from, file_to):
    df = pd.read_csv(file_from,encoding='utf-8')
    index_list = get_list if len(get_list)>0 else list(range(len(df['url'])))
    field_list = []
    for i in range(len(df['url'])):
        try:
            data_rq = rq.get(df['url'][i])
            data_soup = BeautifulSoup(data_rq.text,features="lxml")
            data_pdf = data_soup.select('#pdfContainer')
            df['url_pdf'][i] = data_pdf[0]['src']
        except Exception as e:
            field_list.append(i)
            print('get url['+str(i)+'] failed. Error: '+str(e))
        else:
            print('get pdf url from url['+str(i)+']...')
            # print(df)
    df.to_csv(file_to,encoding='utf-8')

    return field_list


if __name__ == '__main__':
    # save_dir_prefix()
    field_list = get_pdf_url([],'urls.csv','urls_pdf.csv')