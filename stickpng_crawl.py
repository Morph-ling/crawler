#coding:utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import logging
from requests import request
from urlparse import  urlparse
import urllib
import urllib2
from bs4 import BeautifulSoup as Bs
from collections import Counter
import lxml
import json
import datetime
import xlsxwriter
import re
import ssl
from lxml import etree
import cookielib
import threading
import time
import Queue
import inspect
import ctypes
from datetime import datetime
import os
import zipfile
import shutil

#日志
logger = logging.getLogger("simple_example")
logger.setLevel(logging.DEBUG)
#输出到屏幕
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
#输出到文件
fh = logging.FileHandler('new_sucai.log')
fh.setLevel(logging.INFO)
#设置日志格式
fomatter = logging.Formatter('%(asctime)s -%(name)s-%(levelname)s-%(module)s:%(message)s')
ch.setFormatter(fomatter)
fh.setFormatter(fomatter)
logger.addHandler(ch)
logger.addHandler(fh)

#忽略ssl证书
#ssl._create_default_https_context = ssl._create_unverified_context

#首页
index_url = r'http://www.stickpng.com'
#图片链接
img_url = r'http://www.stickpng.com/img/'

cats = ['Animals','At the Movies','Bots and Robots','Celebrities','Clothes','Comics and Fantasy',
'Electronics','Food','Furniture','Games','Holidays','Icons Logos Emojis',
'Kitchenware','Memes','Miscellaneous','Music Stars','Nature','Objects',
'People','Religion','Sports','Tools and Parts','Transport','World Landmarks',
'Youtubers']

headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)'
        'Chrome/45.0.2454.85 Safari/537.36 115Browser/6.0.3',
        'Host': 'www.stickpng.com',
        'Connection': 'keep-alive',
        'Origin': 'http://www.stickpng.com'
    }

cookieJar=cookielib.CookieJar()
opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar))

# 获取图片详情地址
def get_imgs(url,f):
    try:
        request = urllib2.Request("http://www.stickpng.com"+url, headers = headers);
        result = opener.open(request,timeout=5).read();
        content_xpath=etree.HTML(result)
        page_total = json.loads(content_xpath.xpath('//*[@id="pagination"]/attribute::data-pagination')[0])["total"];
        for page in range(1,page_total+1):
            request = urllib2.Request("http://www.stickpng.com"+url+"?page="+str(page), headers = headers);
            result = opener.open(request,timeout=5).read();
            content_xpath=etree.HTML(result)
            new_urls = content_xpath.xpath('//*[@id="results"]/*[@class="item"]/a/attribute::href');
            for new_url in new_urls:
                new_url = new_url.replace("?page=1","");
                if '/img/' not in new_url:
                    get_imgs(new_url.replace("?page=1",""),f)
                else:
                    print new_url;
                    f.write(new_url+'\n');
    except Exception as e:
        return;

# 下载图片
root = "";#文件根目录位置（默认当前目录）
def download_imgs(url):
    try:
        dir_path = url.replace("\n","");
        dir_path = dir_path.replace("/img/","");
        dir_path = root + dir_path;
        is_exists=os.path.exists(dir_path)
        if not is_exists:
            os.makedirs(dir_path);
        request = urllib2.Request("http://www.stickpng.com"+url, headers = headers);
        result = opener.open(request,timeout=5).read();
        content_xpath=etree.HTML(result);
        img = content_xpath.xpath('//*[@id="image"]/*[@class="image"]/img/attribute::src')[0];
        #读取图片
        request = urllib2.Request("http://www.stickpng.com"+img, headers = headers);
        result = opener.open(request,timeout=5)
        f = open(dir_path+img[img.rindex("/"):len(img)], 'wb')
        f.write(result.read())
        f.close()
    except Exception as e:
        print e

def crawl():
    # logger.info('获取图片详情地址');
    # f = open("stickpng_img_urls.txt",'a+');
    # for cat in cats:
    #     cat = cat.replace(" ", "-").lower();
    #     get_imgs("/cat/" + cat,f);
    # f.close()

    # logger.info('下载图片');
    # f = open("stickpng_img_urls.txt",'r');
    # line = f.readline()
    # while line: 
    #     download_imgs(line);
    #     line = f.readline();
    #     break;
    # f.close()

if __name__ == '__main__':
    crawl()








