# -*- coding: utf-8 -*-
# DB: mongodb

from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
import requests,os,re,time,random,urllib.request
import json
import csv
import pandas as pd

header_list=[
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
]

target_url = "http://www.imdb.com/title/tt4154796/?ref_=fn_al_tt_1"
target_url = "https://www.imdb.com/search/title?count=100&release_date=2015,2018&title_type=feature"
target_url = "https://www.imdb.com/search/title?title_type=feature&release_date=2010-01-01,2019-05-01&count=200&start={}1&ref_=adv_nxt"
target_url = "https://www.imdb.com/search/title/?title_type=feature&view=simple&ref_=adv_prv&release_date=2019-05-01,2019-08-01&count=200"
collection = {}

db_api = "http://www.omdbapi.com/?apikey=9be27fce&i=" # i:id, t:title

static_path = r"D:\MovieRS\MRS\static\res\movies"

def crawl(url):
    try:
        randomnum = random.uniform(0,len(header_list))
        totalnum = int(randomnum)
        header={'User-Agent' : header_list[totalnum]}
        res = requests.get(url,headers=header)
        html = res.text
        #html = html.encode("utf-8") #source
        soup = BeautifulSoup(html,"lxml")
    except Exception as e:
        raise e
    else:
        pass

    if soup==[]:
        print ("Target Html has nothing.")

    #details

    movie_title = soup.find_all("div",class_="title_wrapper")
    movie_url = soup.find_all("a",{'href': re.compile(r'^/title/tt.*/?ref_=adv_li_tt')})

    print (len(movie_url))
    pattern = re.compile(r'tt\d+')
    with open("new_indexes.txt","a+",encoding="utf-8") as w:
        for u in movie_url:
            # print (u['href'])
            # print (type(u.text))
            t = str(u['href'])
            m = pattern.findall(t)
            tar = m[0]
            print(tar)
            w.write(tar+"\n")


    #document.querySelector
    # ('#title-overview-widget > div.vital >
    #  div.title_block > div > div.titleBar >
    #  div.title_wrapper > h1')


    # movie_poster = soup.find_all("div",classs_="poster")
    #title-overview-widget > div.vital >
    #  div.slate_wrapper > div.poster >
    #  a > img

    # title_name = title+"Poster"
    # movie_poster = soup.find_all("img",title=title_name)
    # poster_url = movie_poster[0]

    # movie_type = soup.find_all("a",{'href': re.compile(r'^/search/title?genres=.*&ref_=tt_ov_inf')})

    # movie_desc = soup.find_all("div",classs_="summary_text")

    # print (time.strftime("%Y-%m-%d %H:%M:%S"))

    #integration
    # if data:
    #     xxx = data[0]
    #     collection[]=
    # if data:
    #     xxx = data[0]
    #     collection[]=
    # if data:
    #     xxx = data[0]
    #     collection[]=
    # if data:
    #     xxx = data[0]
    #     collection[]=
    # if data:
    #     xxx = data[0]
    #     collection[]=
    return soup
def getcontent(api):
    try:
        randomnum = random.uniform(0,len(header_list))
        totalnum = int(randomnum)
        header={'User-Agent' : header_list[totalnum]}
        res = requests.get(api,headers=header)
        resource = res.text
        content = json.loads(resource)
        #html = html.encode("utf-8") #source
        #soup = BeautifulSoup(html,"lxml")
    except Exception as e:
        raise e
    else:
        pass
    # return content.get("Title")
    return content
def getfilename(path): #poster_dir, filename
    container=[]
    for filename in os.listdir(path):
        fp = os.path.join(path, filename)
        if os.path.isfile(fp):
            # file_dir =os.path.join(path)+"/"+filename
            filename = filename.replace('.jpg','')
            if(len(filename)==6):
                filename = "0"+filename
            elif(len(filename)==5):
                filename = "00"+filename
            container.append(filename)
    return (container)
def getfolder(path,folder_set=[]):
    for f in os.listdir(path):
        fp = os.path.join(path, f)
        if os.path.isdir(fp):
            thedir = f
            folder_set.append(thedir)
    return folder_set

if __name__ == '__main__':
    '''
    """save info into file """
    dir_set = {}
    m_table = {}
    for f in (getfolder(static_path)): #得到所有的type名称和type文件夹地址
        movie_type = f
        movie_type_dir = static_path+"\\"+f
        dir_set[movie_type] = movie_type_dir

    for genre in dir_set.keys(): #每一个类别
        print ("Genre: "+genre)
        for ix in getfilename(dir_set.get(genre)): #通过所有的type文件夹地址
                                                   #得到所有的file名字
            time.sleep(0.2)
            poster_url = getcontent(db_api+str("tt"+ix)) #通过file名字得到content
            while (poster_url == None):
                time.sleep(0.5)
                poster_url = getcontent(db_api+str("tt"+ix))
            m_table[ix] = poster_url
            print (poster_url)

    # --------------
    """save json data """
    data = json.dumps(m_table,ensure_ascii=False)
    with open("poster.json","w+",encoding="utf-8") as out:
        out.write(data)

    print("Done!")
    '''
    """read json data """
    # with open("latest_movies.json","r",encoding="utf-8") as inp:
    #     data = inp.read()
    #     dataset = json.loads(data)
    # print (len(dataset))

    #```````````````````````` 保存网页
    # print ("\n"+target_url)
    # soup = crawl(target_url)
    # with open("soup.html","w+",encoding="utf-8") as f:
    #     f.write(str(soup))
    # print("Done")
    soup = crawl(target_url)
    print("Done")
    #```````````````````````` 读取
    # with open("soup.html","r",encoding="utf-8") as s:
    #     soup = BeautifulSoup(s.read(), "lxml")
    # movie_header = soup.find_all("h3",class_="lister-item-header")
    # content = index= ""
    # for item in movie_header:
    #     try:
    #         content = item.contents[3]
    #     except Exception as e:
    #         print("no detail item..")
    #         #_content = item.text
    #     if content:
    #         title = content.text
    #         index = content.attrs.get("href").replace("/?ref_=adv_li_tt","").replace("/title/","")
    #     print (index,title)
    # print("Done!")

    #crawl new 1k movies from 2010 to 2019
    '''
    m_table = {}
    for nu in range(8):
        content = index= ""
        if nu!=0:
            url = target_url.format(str(nu)+"0")
            time.sleep(1)
        else:
            url = target_url.format("")
        print(".................................")
        print(nu)
        print(url)

        soup = crawl(url)
        movie_header = soup.find_all("h3",class_="lister-item-header")
        for item in movie_header:
            try:
                content = item.contents[3]
            except Exception as e:
                print("no detail item..")
                #_content = item.text
            if content:
                index = content.attrs.get("href").replace("/?ref_=adv_li_tt","").replace("/title/","")
                title = content.text
            m_table[index] = title
            print (index,title)

    data = json.dumps(m_table,ensure_ascii=False)
    with open("latest_movies.json","w+",encoding="utf-8") as out:
        out.write(data)
    print("Done.......")
    '''


    """read json data """
    # with open("latest_movies.json","r",encoding="utf-8") as inp:
    #     data = inp.read()
    #     dataset = json.loads(data)

    # print (len(dataset))

    # new_container = {}

    '''save csv file'''
    # count = 0
    # csv_file = "imdbID,Title,Released,Genre,Poster\n"
    # for index in dataset.keys():
    #     genre = ""
    #     count +=1
    #     time.sleep(0.1)
    #     print (count,index)
    #     response = getcontent(db_api+str(index))
    #     title = response.get("Title")
    #     released = response.get("Year")
    #     genre_string = response.get("Genre")
    #     genres = genre_string.split(",")
    #     img = response.get("Poster")

    #     # detail.append(index)
    #     # detail.append(title)
    #     # detail.append(released)
    #     # detail.append(genres)
    #     # detail.append(img)
    #     csv_file += str(index)+","
    #     csv_file += str(title)+","
    #     csv_file += str(released)+","
    #     csv_file += str(img)+","
    #     for char in str(genres):
    #         if char ==",":
    #             char = "&"
    #         if char ==" ":
    #             char =""
    #         genre += str(char)
    #     csv_file += str(genre)+","

    #     csv_file += "\n"
    # with open("Bigcollection.csv","w+") as outp:
    #     outp.write(str(csv_file))
    # print("Save successfully..")

    # content = pd.read_csv("Bigcollection.csv")
    # print (content)

    # with open("Bigcollection.csv","r") as fi:
    #     # content = csv.reader(fi.read())

#   0    1     2
# Title Year Genre
#   1        [xx,xx]
#   2        [xx,xx]
#   3        [xx,xx]
###############

# csv file
# json
# bin


