from django import template
from user import views as v
# from user.models import Resulttable as rt

register = template.Library()


@register.filter
def check_index(i):
    if(i[0]=='0'):
        if(i[1]=='0'):
            i=i[2:]
        else:
            i=i[1:]
    return i

@register.filter
def get_value(con,key):
    return con.get(key)

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