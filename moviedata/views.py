from django.shortcuts import render
from django.shortcuts import render_to_response
import json,os,requests

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
static_path = BASE_DIR + r"\static\res\movies"
db_api_t = "http://www.omdbapi.com/?apikey=9be27fce&t={}"
db_api_i = "http://www.omdbapi.com/?apikey=9be27fce&i={}"

def getcontent(param,useid=False):# 获取api json
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
def detail(request,template_name): #bug
    param = request.GET.get("title")
    data = getcontent(param)
    return render_to_response(template_name,data)
def detailbyid(request,template_name): #bug
    param = request.GET.get("id")
    data = getcontent(param,useid=True)
    return render_to_response(template_name,data)
