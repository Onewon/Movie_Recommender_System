from __future__ import absolute_import, unicode_literals
from celery import shared_task

# from gevent import monkey
# monkey.patch_all()
import gevent

import requests
import json

# import sys,io
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8')

def get_movie_detail(param,use_movieid=False):
    db_api_t = "http://www.omdbapi.com/?apikey=9be27fce&t={}"
    db_api_i = "http://www.omdbapi.com/?apikey=9be27fce&i={}"
    if(use_movieid==True):
        db_api_t = db_api_i
    url = db_api_t.format(param)
    return url

def crawl(url):
    header = {'User-Agent' : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"}
    res = requests.get(url,headers = header)
    return res.text

# crawl.delay(url,header = header)
@shared_task
def a_crawl(url):
    header = {'User-Agent' : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"}
    res = requests.get(url,headers = header)
    return res.text
@shared_task
def fetchAllRated(rating_record):
    if type(rating_record) == dict:
        url_list = [get_movie_detail(m,True) for m in rating_record.keys()]
    jobs = [gevent.spawn(crawl,url) for url in url_list]
    gevent.joinall(jobs,timeout=2)
    detail = [worker.get() for worker in jobs]
    res = []
    for d in detail:
        if type(d) == str:
            do = eval(d)
        mid = do.get("imdbID")
        do["rating"] = rating_record.get(mid)
        res.append(do)
    return res
@shared_task
def fetchAllRecom(url_list):
    # url_list = ['tt1211837','tt0948470']
    url_list = [get_movie_detail(m_index,True) for m_index in url_list]
    jobs = [gevent.spawn(crawl,url) for url in url_list]
    gevent.joinall(jobs,timeout=2)
    return [worker.get() for worker in jobs]

# @shared_task
# def crawl_and_get(url):
#     resp = gevent.spawn(requests.get, url,headers = header)
#     tmp = 0
#     print('wait...', tmp)
#     if resp.ready():
#         resource = resp.text
#         content = json.loads(resource)
#         return content
#         # return 'from:' + socket.getfqdn() + '\nres:' + str(resp.value.text)
#     gevent.sleep(0)
#     tmp += 1
