from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.template import Template,Context
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views.generic import TemplateView
import json,requests,os
from .forms import RegisterForm
from user.models import Resulttable as rt
from user.models import Users_detail as ur
from django.db.models import Q
from user.tasks import add

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
static_path = BASE_DIR + r"\static\res\movies"

def getfolder(path,folder_set=[]):
    for f in os.listdir(path):
        fp = os.path.join(path, f)
        if os.path.isdir(fp):
            thedir = f
            folder_set.append(thedir)
    return folder_set
def getfilename(path): #poster_dir, filename
    container=[]
    for filename in os.listdir(path):
        fp = os.path.join(path, filename)
        if os.path.isfile(fp):
            # file_dir =os.path.join(path)+"/"+filename
            filename = filename.replace('.jpg','')
            # if(len(filename)==6):
            #     filename = "0"+filename
            # elif(len(filename)==5):
            #     filename = "00"+filename
            container.append(filename)
    return (container)

dir_set = {}
genre_set = {}
for f in (getfolder(static_path)): #
    movie_type = f
    movie_type_dir = static_path+"\\"+f
    dir_set[movie_type] = movie_type_dir      #{genre: [path],....}

for genre in dir_set.keys(): #
    # print ("Genre: "+genre)
    con = []
    for ix in getfilename(dir_set.get(genre)): #
        con.append(ix)                         #
    genre_set[genre] = con                     # {genre: [index.....], .....}
with open(BASE_DIR +"/static/res/title_index.json","r",encoding="utf-8") as inp:
    data = inp.read()
    dataset = json.loads(data)

#target data:
# img : url -> path+filename FROM filename/ poster.json
# genre -> identify FROM genre_set
# title -> FROM dataset.get(index)
class IndexView(TemplateView):
    template_name = 'index.html'
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['item_list'] = ["Action","Animation","Comedy","Crime","Drama",
        "Love","Science fiction","Thriller","War"]
        # context['item_list'] = ["Action","Animation","Comedy","Crime","Drama",
        # "Love","Science fiction","Thriller",
        # "Biography","Family","History","Horror","Music","War",]
        # context['item_list'] = ["Action","Horror","Comedy","Animation","Science fiction","Crime","Love"]
        context['genres'] = genre_set #
        context['titleset'] = dataset #
        return context

# def index(request,template_name):
#     return render_to_response(template_name,{"data":"content"})

def search(request):
    param = request.GET.get("imdb")
    result = add.delay(2, 3) # asyn try
    #return HttpResponse(param1)
    return HttpResponseRedirect("https://www.imdb.com/find?ref_=nv_sr_fn&q="+param+"&s=all")
    # context={'data': param1,}
    # return render(request, 'display.html', context)
def search_detail(request):
    param = request.GET.get("q")
    return HttpResponseRedirect("/moviedetail/search?title="+param)
    #return HttpResponseRedirect("http://www.omdbapi.com/?&t="+param+"&apikey=9be27fce")
def register(request):

    if request.method == 'POST':

        form = RegisterForm(request.POST)

        #
        if form.is_valid():
            #
            user = form.save()

            #
            # user = authenticate(username=form["username"], password=form["password1"])
            # auth.login(request, user)
            request.session.set_expiry(0)
            login(request,user)
            return redirect('/')
    else:
        #
        form = RegisterForm()

    #
    return render(request, 'registration/register.html', context={'form': form})
def rating(request):
    if request.method=="POST":
        rating_form = request.POST
        USERID = int(rating_form["userid"]) +1000
        IMDBID = str(rating_form["movieid"])
        MOVIE_RATING = float(rating_form["rating"])
        # rt.objects.create(userid=USERID,rating_Movieid=IMDBID,rating=MOVIE_RATING)
        obj, created = rt.objects.update_or_create(
            userid=USERID,rating_Movieid=IMDBID,
            defaults={'rating': MOVIE_RATING},
        )
    else:
        pass
    #return render(request, 'index.html',{'userId':USERID,'rating':RATING,'imdbId':IMDBID})
    return HttpResponseRedirect('/')

def deleteRating(request):
    if request.method=="POST":
        del_form = request.POST
        USERID = int(del_form["USERID"]) +1000
        IMDBID = str(del_form["DELMOVIE"])
        # rt.objects.create(userid=USERID,rating_Movieid=IMDBID,rating=MOVIE_RATING)
        # obj, created = rt.objects.update_or_create(
        #     userid=USERID,rating_Movieid=IMDBID,
        #     defaults={'rating': MOVIE_RATING},
        # )
        rt.objects.filter(userid=USERID,rating_Movieid=IMDBID).delete()
    else:
        pass
    #return render(request, 'index.html',{'userId':USERID,'rating':RATING,'imdbId':IMDBID})
    return HttpResponseRedirect('/')

def getprofiledetail(request):
    userID = "10"+request.GET.get("id")
    profile = ur.objects.filter(userid=userID)
    if len(profile)==0:
        nickname=""
        gender=""
        birthyear=""
        prefer=""
    else:
        profile = profile[0]
        nickname = profile.nickname
        gender= profile.gender
        birthyear= profile.birthyear
        prefer= profile.prefer

    return render(request, 'profile.html',
    {
        "NIKENAME": nickname,
        "GENDER": gender,
        "BIRTH": birthyear,
        "PREFER": prefer,
    })

def updateprofile(request):
    if request.method=="POST":
        profile_form = request.POST
        USERID = int(profile_form["USERID"])
        NIKENAME = str(profile_form["NIKENAME"])
        GENDER = str(profile_form["GENDER"])
        BIRTH =  str(profile_form["BIRTHYEAR"])
        PREFER = str(profile_form["PREFER"])
        obj, created = ur.objects.update_or_create(
            id=USERID,
            defaults={
            'nickname': NIKENAME,
            'gender': GENDER,
            'prefer': PREFER,
            'birthyear': BIRTH,
            'userid': USERID+1000,
            },
        )
    else:
        pass
    #return render(request, 'index.html',{'userId':USERID,'rating':RATING,'imdbId':IMDBID})
    return HttpResponseRedirect('/')

