from django.shortcuts import render
from django.shortcuts import render_to_response
import json,os,requests
from django.views.generic import TemplateView
from .models import Moviestable as mt
from user.models import Resulttable as rt

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
    return render(request, 'profile.html',{'container':con})

def recom1(request):
    if request.method=="POST":
        form = request.POST
        USERID = int(form["USERID"])+1000
    else:
        pass
    return render(request, 'result_user.html',{})
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