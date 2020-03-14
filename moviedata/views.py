from django.shortcuts import render
from django.shortcuts import render_to_response
import json,os,requests,time
from django.views.generic import TemplateView
from .models import Moviestable as mt
from MRS.settings import BASE_DIR as b_dir
from user.models import Resulttable as rt
import numpy as np
import pandas as pd
from sklearn.preprocessing import scale
# import time,json,os
import pprint as pp
# from scipy.sparse import dia_matrix,coo_matrix,lil_matrix

Res_list = {}
from sqlalchemy import create_engine

class Usercf():
    def __init__(self):
        self.path = b_dir+r"\static\res\csv\ratings_base.csv"
        self.link_path = b_dir+r"\static\res\csv\links_latest.csv"
        self.rating_filename = r"pre_user_rating.npy"
        self.movie_link = pd.read_csv(self.link_path)
        #self.wateched_list = {}
        self.watch_list = []
        self.themap = {} #
        self.movie_num = 194326 #194126 # total movie matrix col ,depend movie number of the link.csv
        self.total_user_num = 610 # based on the length of ratings.csv
        # self.end_id = 610
    # rating.csv, links.csv, watched_list

    # read user result
    def readresult(self,userid):
        engine = create_engine('mysql+pymysql://root:123456@localhost:3306/userinfo')
        sql = "select * from user_resulttable"
        rt = pd.read_sql_query(sql, engine)
        target_index = rt[rt["userid"] == str(userid)]["rating_Movieid"].tolist()
        rating_index = rt[rt["userid"] == str(userid)]["rating"].tolist()

        imdb_and_rating = []
        preferred_movies_imdb = []
        for i in target_index:
            i = i.replace("tt","")
            preferred_movies_imdb.append(int(i)) #

        imdb_and_rating.append(preferred_movies_imdb) #imdbID
        imdb_and_rating.append(rating_index) #rating
        return imdb_and_rating

    # imdb to normal
    def imdb2normal(self,box):
        rating_map = {}
        preferred_movies = []
        missing_index = [] #没有links的movie index
        for index in box[0]:
            id_imdb = self.movie_link[self.movie_link["imdbId"] == index]["movieId"].tolist()
            if len(id_imdb)==0:
                missing_index.append(index)
                continue
            preferred_movies.append(int(id_imdb.pop()))
        #print ("Missing index has "+str(len(missing_index)))
        for i,rating in enumerate(box[-1]):
            rating_map[preferred_movies[i]] = rating
        return rating_map

    # normal to imdb
    def normal2imdb(self,box):
        preferred_imdb_movies = []
        missing_index = [] #没有links的movie index
        for index in box:
            id_n = self.movie_link[self.movie_link["movieId"] == index]["imdbId"].tolist()
            if len(id_n)==0:
                missing_index.append(index)
                continue
            theindex = str(id_n.pop())
            while len(theindex)<7:
                theindex = "0"+theindex
            preferred_imdb_movies.append("tt"+theindex)
        #print ("Missing index has "+str(len(missing_index)))
        return preferred_imdb_movies

    #numpy cal
    def np_cal(self,user_rating):
        x = np.mat(user_rating) # format: userid,movieid,rating
        x_s = scale(x, with_mean=True, with_std=True, axis=1)
        # Standardize dataset, eliminate the distraction of extreme value

        y = x_s.dot(x_s.transpose())# dot product, numerator
        v = np.zeros((np.shape(y)[0], np.shape(y)[1]))
        v[:] = np.diag(y) # denominator
        us = y/v# obtain User Similarity Matrix US

        usp = np.mat(us).dot(x_s)# According to similarity between user,come out with USP matrix.
        usr = np.sum(us, axis=1)# denominator
        p = np.divide(usp, np.mat(usr).transpose())
        # Division of corresponding elements, Normalization get the preference matrix of user
        return p

    #cal similarity
    def sim_index(self,path,additive):
        # start time
        time_start = time.time()
        npypath = b_dir + "\\" + self.rating_filename # speed up
        if not os.path.isfile(npypath):
            df = pd.read_csv(path) #read file
            user_num = df["userId"].max()
            user_rating = np.zeros((user_num+1, self.movie_num))
            df["userId"] = df["userId"] - 1
            df["movieId"] = df["movieId"] - 1

            for index in range(user_num):
                user_rating[index][df[df["userId"] == index]["movieId"]] = df[df["userId"] == index]["rating"]

            #save npy
            np.save(self.rating_filename,user_rating)
        else:
            user_rating = np.load(self.rating_filename)

        index = self.total_user_num-1
        #--------------add my user into user_rating and load wateched_list---------------------
        for m,r in additive.items():
            user_rating[index+1][m-1] = r #index+1
        p = self.np_cal(user_rating) # recom cal

        # end time
        time_end = time.time()

        print("Calculating time spends:", time_end - time_start)
        return p

from .tasks import a_crawl
from .tasks import fetchAllRecom as fetchAll
from .tasks import fetchAllRated
#backup: 4ee790e0/d82cb888/386234f9/d58193b6/15c0aa3f
def getcontent(param,use_movieid=False):# get api json
    db_api_t = "http://www.omdbapi.com/?apikey=9be27fce&t={}"
    db_api_i = "http://www.omdbapi.com/?apikey=9be27fce&i={}"
    content = {}
    if(use_movieid==True):
        db_api_t = db_api_i
    try:
        url = db_api_t.format(param)

        # header = {'User-Agent' : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"}
        # res = requests.get(url,headers = header)
        # resource = res.text
        # content = json.loads(resource)
        # return content

        resource = a_crawl.delay(url).get() ## share_task
        content = json.loads(resource)
        return content
    except Exception as e:
        raise e
    else:
        pass

def getprofile(request): #for empty user, has bugs.
    con = []
    if request.method=="POST":
        rating_form = request.POST
        USERID = int(rating_form["USERID"])+1000
        CELERY_connector = dict()
        for query_rs in rt.objects.filter(userid = USERID):
            CELERY_connector[query_rs.rating_Movieid] = query_rs.rating
        con = fetchAllRated.delay(CELERY_connector).get()
        # for record in rt.objects.filter(userid = USERID):
        #     response = getcontent(record.rating_Movieid,True)
        #     response["rating"] = record.rating
        #     con.append(response)
    else:
        pass
    return render(request, 'history.html',{'container':con})

# def getprofiledetail(request):
#     return render(request, 'profile.html',{})

def Sorting(dicts):
    indexs = [i for i in dicts.keys()]
    length=len(indexs)
    for i in range(length-1):
        for j in range(length-1):
            if dicts.get(indexs[j])>dicts.get(indexs[j+1]):
                indexs[j],indexs[j+1]=indexs[j+1],indexs[j]
    # new_dict = {}
    # for i in indexs:
    #     new_dict[i] = dicts.get(i)
    return indexs
# def bubble_sort(array):
#     length=len(array)
#     for i in range(length-1):
#         for j in range(length-1):
#             if array[j]>array[j+1]:
#                 array[j],array[j+1]=array[j+1],array[j]
#     return array

def recom(request): #Recommendation function
    if request.method=="POST":
        form = request.POST
        USERID = int(form["USERID"])+1000 #userid
    else:
        pass
    #timer start
    time_start = time.time()
    random_dict = {}
    resmovies_list = []

    #recommendation part
    usercf = Usercf()
    imdb_list = usercf.readresult(USERID) #read user rating from MySQL, based on imdb ID.
    normal_map = usercf.imdb2normal(imdb_list)
    for k in normal_map.keys():
        usercf.watch_list.append(int(k-1)) # index minus 1

    p = usercf.sim_index(usercf.path,normal_map)

    target_person = p[usercf.total_user_num] # the preferred movie list of target user

    it = np.nditer(target_person, flags=['f_index'], op_flags = ['readwrite'])
    while not it.finished:
        usercf.themap[it.index] = str(np.format_float_positional(it[0]))
        it.iternext()
    for index,value in usercf.themap.items():
        v = float(value)
        #del watched
        if((index) in usercf.watch_list):
            continue

        #the mark line
        if(v>=10.0):
            random_dict[index+1] = v
    resmovies_list = Sorting(random_dict)
    # imdb to normal
    resmovies_list = usercf.normal2imdb(resmovies_list) #corresponding imdb
    resdetail_list = []
    if resmovies_list!=[]:
        resdetail_list = fetchAll.delay(resmovies_list[::-1]).get() # async faster
        # for item in resmovies_list[::-1]:
        #    content = getcontent(item,True) #cost time
        #    resdetail_list.append(content) # a list contains many json 
    else:
        print("Can not come out with recommendation data.")
    #timer end
    time_end = time.time()
    print ("Loading posters spends: "+str(round(time_end - time_start,2)))
    return render(request, 'result_user.html',
    {"Res":resdetail_list,"ResponseTime": str(round(time_end - time_start,2))})

# def recom2(request):
#     if request.method=="POST":
#         form = request.POST
#         USERID = int(form["USERID"])+1000
#     else:
#         pass

#     return render(request, 'result_item.html',{})


class detailView(TemplateView):
    template_name = 'movie_detail.html'
    def get_context_data(self, **kwargs):
        param = self.request.GET.get("title")
        data = getcontent(param)
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context['Poster'] = data.get("Poster")
        context['Title'] = data.get("Title")
        context['Released'] = data.get("Released")
        context['Runtime'] = data.get("Runtime")
        context['Plot'] = data.get("Plot")
        context['Genre'] = data.get("Genre")
        context['Actors'] = data.get("Actors")
        context['Director'] = data.get("Director")
        context['Language'] = data.get("Language")
        context['Country'] = data.get("Country")
        context['index'] = data.get("imdbID")
        context['Type'] = data.get("Type")
        context['Website'] = data.get("Website")
        return context

class detailbyIDView(TemplateView):
    template_name = 'movie_detail.html'
    def get_context_data(self, **kwargs):
        param = self.request.GET.get("id")
        data = getcontent(param,True)
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context['index'] = param
        context['Poster'] = data.get("Poster")
        context['Title'] = data.get("Title")
        context['Released'] = data.get("Released")
        context['Runtime'] = data.get("Runtime")
        context['Plot'] = data.get("Plot")
        context['Genre'] = data.get("Genre")
        context['Actors'] = data.get("Actors")
        context['Director'] = data.get("Director")
        context['Language'] = data.get("Language")
        context['Country'] = data.get("Country")
        context['Type'] = data.get("Type")
        context['Website'] = data.get("Website")
        return context

class RecommendView(TemplateView):
    template_name = 'recommend.html'
    def get_context_data(self, **kwargs):
        USERID = int(self.request.GET.get("user"))+1000
        num_of_objects = int(rt.objects.filter(userid=USERID).count())
        context = super().get_context_data(**kwargs)
        context['rating_movies'] = num_of_objects
        return context

# class Recommend_User_View(TemplateView):
#     template_name = 'result_user.html'
#     def get_context_data(self, **kwargs):
#         USERID = int(self.request.GET.get("user"))+1000
#         context = super().get_context_data(**kwargs)
#         context['rating_movies'] = 0
#         return context

# class Recommend_Item_View(TemplateView):
    # template_name = 'result_item.html'
    # def get_context_data(self, **kwargs):
    #     USERID = int(self.request.GET.get("user"))+1000
    #     context = super().get_context_data(**kwargs)
    #     context['rating_movies'] = 0
    #     return context