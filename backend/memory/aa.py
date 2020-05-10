import json
import time
import urllib

import jsonpath as jsonpath
import requests  # 用于获取网页
from bs4 import BeautifulSoup  # 用于分析网页

import os,django

from django.db import transaction
from numpy import unicode

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()
from memory.models import News


def timeStamp(timeNum):
    timeStamp = float(timeNum / 1000)
    timeArray = time.localtime(timeStamp)
    return time.strftime("%Y-%m-%d %H:%M:%S", timeArray)


# 获取网页
keyword = '阿兹海默症'
number = 50
# print(requests.request('POST','https://search.sohu.com/?keyword='+ urllib.parse.quote(keyword) +'&spm=smpc.csrpage.0.0.1588323312046VQCPSPF&queryType=outside').text)
# requests.request('POST','https://search.sohu.com/?keyword='+ urllib.parse.quote(keyword) +'&spm=smpc.csrpage.0.0.1588323312046VQCPSPF&queryType=outside')
print(requests.get('https://search.sohu.com/?keyword=' + urllib.parse.quote(
    keyword) + '&spm=smpc.csrpage.0.0.1588323312046VQCPSPF&queryType=outside').text)

baseurl = 'https://search.sohu.com/search/meta?keyword=' + urllib.parse.quote(
    keyword) + '&terminalType=pc&ip=43.227.138.213&city=%E5%9B%BD%E5%86%85%E6%9C%AA%E8%83%BD%E8%AF%86%E5%88%AB%E7%9A' \
               '%84%E5%9C%B0%E5%8C%BA&spm-pre=smpc.csrpage.0.0.1588323312046VQCPSPF&SUV=2004111239209035&from=0&size' \
               '=' + str(
    number) + '&searchType=news&queryType=outside&queryId=15883240752136Zi%2F006&pvId=1588324074066V829d2V&refer' \
              '=https%3A//search.sohu.com/%3Fkeyword%3D%25E9%2598%25BF%25E5%2585%25B9%25E6%25B5%25B7%25E9%25BB%2598' \
              '%25E7%2597%2587%26source%3Darticle%26queryType%3Dedit%26ie%3Dutf8%26spm%3Dsmpc.content.search-box.1' \
              '.1588323302443HwZMJSm&size=10&maxL=15&spm=&_=' + str(
    int(round(time.time() * 1000)))

html = requests.get(baseurl)
unicodestr = json.loads(html.text)

title_list = jsonpath.jsonpath(unicodestr, "$..title")
summary_list = jsonpath.jsonpath(unicodestr, "$..briefAlg")
author_list = jsonpath.jsonpath(unicodestr, "$..authorName")
# image_list =jsonpath.jsonpath(unicodestr, "$..images")
time_list = jsonpath.jsonpath(unicodestr, "$..postTime")
url_list = jsonpath.jsonpath(unicodestr, "$..url")

print(len(title_list))
for i in range(len(title_list)):
# for i in range(1):
    try:
        with transaction.atomic():
            childhtml = requests.get(url_list[i])
            soup = BeautifulSoup(childhtml.text, 'lxml')
            article = soup.find('article')
            if article is None:
                print('content is none')
                continue
            if News.objects.filter(title=title_list[i]).exists():
                print('has exist')
                continue
            news = News.objects.create()
            news.title=title_list[i]
            news.summary=summary_list[i]
            news.author=author_list[i]
            news.time=timeStamp(time_list[i])
            # news.content=str(article).encode('utf-8').decode('utf-8','ignore')
            news.content = str(article)
            news.origin='网络'
            news.save()
            print('add success')
    except:
        print('error')
        continue
    # finally:
    #     print('finnal')
    #
    # print(title_list[i])
    # print(summary_list[i])
    # print(author_list[i])
    # print(time_list[i])
    # print(url_list[i])
    # print(article)

print('抓取完毕')
