from django import template
from user import views as v
import random
# from user.models import Resulttable as rt

register = template.Library()

@register.filter
def check_index(i): #使用新的img集时就不需要了
    if(i[0]=='0'):
        if(i[1]=='0'):
            i=i[2:]
        else:
            i=i[1:]
    return i

@register.filter
def get_value(con,key):
    return con.get(key)

@register.filter
def rangeoflist(container):
    random_start = random.uniform(1,50)
    r_s = int(random_start)
    r_e = r_s + 16
    # return container[r_s:r_e]
    return container[r_s:r_e]
    # return container[:16]

# @register.filter
# # def mark(userid,movie,rating):
# def mark(idset,rating):
#     usermark = rt(userid=idset[0],rating_Movieid=idset[1],rating=rating)
#     usermark.save()
# # userid -> imdbID -> rating
# @register.filter
# def maketogether(userid,movieid):
#     idset =[]
#     idset.append(userid)
#     idset.append(movieid)
#     return idset