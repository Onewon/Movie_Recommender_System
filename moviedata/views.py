from django.shortcuts import render
from django.shortcuts import render_to_response
import json,os,requests,time
from django.views.generic import TemplateView
from .models import Moviestable as mt
from user.models import Resulttable as rt
Res_list = {}
l = ['tt1431045','tt2948356','tt2543164','tt3315342','tt1856101','tt0848228', 'tt1345836', 'tt1490017', 'tt0816692', 'tt2015381', 'tt2084970','tt1136608', 'tt0499549', 'tt0892769', 'tt1375666','tt0076759', 'tt0111161', 'tt0109830', 'tt0108052', 'tt0080684', 'tt0093779', 'tt0082971', 'tt0086190', 'tt0120815', 'tt0133093', 'tt0137523', 'tt0120689', 'tt0126029', 'tt0198781', 'tt0120737', 'tt0167261', 'tt0266543', 'tt0325980', 'tt0167260', 'tt0317705', 'tt0372784', 'tt0482571', 'tt0468569', 'tt0371746', 'tt0910970', 'tt0361748', 'tt1049413']
Res_list["1016"] = l
Res_list["1017"] = ['tt0317705', 'tt0372784', 'tt0407887',
 'tt0482571', 'tt0468569', 'tt0371746','tt0910970', 'tt0361748', 'tt1375666', 'tt0816692', 'tt2015381',
'tt0114746', 'tt0114369', 'tt0114814', 'tt0112573', 'tt0112384', 'tt0111161', 'tt0109830', 'tt0110357', 'tt0107290',
  'tt0108052', 'tt0103064', 'tt0102926', 'tt0116282', 'tt0116629','tt0068646', 'tt0080684', 'tt0082971', 'tt0086190', 'tt0088763',
    'tt0097576', 'tt0119217', 'tt0120815', 'tt0133093', 'tt0167404','tt0169547', 'tt0137523', 'tt0172495', 'tt0209144', 'tt0126029', 'tt0198781',
      'tt0120737', 'tt0167261', 'tt0266543', 'tt0325980', 'tt0167260', 'tt0304141',]

#backup: 4ee790e0/d82cb888/386234f9/d58193b6/15c0aa3f
def getcontent(param,useid=False):# 获取api json
    db_api_t = "http://www.omdbapi.com/?apikey=9be27fce&t={}"
    db_api_i = "http://www.omdbapi.com/?apikey=9be27fce&i={}"
    content = {}
    if(useid==True):
        db_api_t = db_api_i
    try:
        header= {'User-Agent' : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"}
        url = db_api_t.format(param)
        res = requests.get(url,headers = header)
        resource = res.text
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
        for record in rt.objects.filter(userid = USERID):
            response = getcontent(record.rating_Movieid,True)
            response["rating"] = record.rating
            con.append(response)
    else:
        pass
    return render(request, 'history.html',{'container':con})

def getprofiledetail(request):
    return render(request, 'profile.html',{})

def recom1(request):
    if request.method=="POST":
        form = request.POST
        USERID = int(form["USERID"])+1000
    else:
        pass
    #timer start
    time_start = time.time()
    resmovies_list = []
    resmovies_list = Res_list.get(str(USERID))
    '''
    #recommendation part
    '''
    resdetail_list = []
    if resmovies_list!=[]:
        for item in resmovies_list:
            content = getcontent(item,True)
            resdetail_list.append(content)
    else:
        pass
    #timer end
    time_end = time.time()
    return render(request, 'result_user.html',{"Res":resdetail_list,"ResponseTime": str(round(time_end - time_start,2))})
def recom2(request):
    if request.method=="POST":
        form = request.POST
        USERID = int(form["USERID"])+1000
    else:
        pass

    return render(request, 'result_item.html',{})

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