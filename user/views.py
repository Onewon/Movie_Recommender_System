from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.template import Template,Context
from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth import authenticate, login
from django.views.generic import TemplateView
import json,requests,os
from user.models import Resulttable as rt


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
            if(len(filename)==6):
                filename = "0"+filename
            elif(len(filename)==5):
                filename = "00"+filename
            container.append(filename)
    return (container)

dir_set = {}
genre_set = {}
for f in (getfolder(static_path)): #得到所有的type名称和type文件夹地址
    movie_type = f
    movie_type_dir = static_path+"\\"+f
    dir_set[movie_type] = movie_type_dir      #{genre: [path],....}
for genre in dir_set.keys(): #每一个类别
    # print ("Genre: "+genre)
    con = []
    for ix in getfilename(dir_set.get(genre)): #通过所有的type文件夹地址
        con.append(ix)                         #得到所有的file名字
    genre_set[genre] = con                     # {genre: [index.....], .....}
with open(BASE_DIR +"/static/res/default_data.json","r",encoding="utf-8") as inp:
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
        context['item_list'] = ["Action","Animation","Comedy","Crime","Drama","Love","Science fiction","Thriller"]
        # context['item_list'] = ["Action","Horror","Comedy","Animation","Science fiction","Crime","Love"]
        context['genres'] = genre_set
        context['titleset'] = dataset
        return context

# def index(request,template_name):
#     return render_to_response(template_name,{"data":"content"})

def search(request):
    param = request.GET.get("imdb")
    #return HttpResponse(param1)
    return HttpResponseRedirect("https://www.imdb.com/find?ref_=nv_sr_fn&q="+param+"&s=all")
    # context={'data': param1,}
    # return render(request, 'display.html', context)

def search_detail(request):
    param = request.GET.get("q")
    return HttpResponseRedirect("/moviedetail/search?title="+param)
    #return HttpResponseRedirect("http://www.omdbapi.com/?&t="+param+"&apikey=9be27fce")

def register(request):
    # 只有当请求为 POST 时，才表示用户提交了注册信息
    if request.method == 'POST':
        # request.POST 是一个类字典数据结构，记录了用户提交的注册信息
        # 这里提交的就是用户名（username）、密码（password）、邮箱（email）
        # 用这些数据实例化一个用户注册表单
        form = RegisterForm(request.POST)

        # 验证数据的合法性
        if form.is_valid():
            # 如果提交数据合法，调用表单的 save 方法将用户数据保存到数据库
            form.save()

            # 注册成功，跳转回首页
            return redirect('/')
    else:
        # 请求不是 POST，表明用户正在访问注册页面，展示一个空的注册表单给用户
        form = RegisterForm()

    # 渲染模板
    # 如果用户正在访问注册页面，则渲染的是一个空的注册表单
    # 如果用户通过表单提交注册信息，但是数据验证不合法，则渲染的是一个带有错误信息的表单
    return render(request, 'registration/register.html', context={'form': form})

def rating(request):
    if request.method=="POST":
        rating_form = request.POST
        USERID = int(rating_form["userid"]) +1000
        IMDBID = str(rating_form["movieid"])
        MOVIE_RATING = float(rating_form["rating"])
        rt.objects.create(userid=USERID,rating_Movieid=IMDBID,rating=MOVIE_RATING)
    else:
        pass
    #return render(request, 'index.html',{'userId':USERID,'rating':RATING,'imdbId':IMDBID})
    return HttpResponseRedirect('/')