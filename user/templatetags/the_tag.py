from django import template
from user import views as v
register = template.Library()

# @register.filter
# def get_at_index(list, index):
#     return list[index]
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
