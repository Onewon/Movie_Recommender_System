from django.contrib import admin
from .models import User,Users_detail,Resulttable

# Register your models here.
admin.site.register(User)
admin.site.register(Resulttable)
admin.site.register(Users_detail)