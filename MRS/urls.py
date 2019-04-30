"""MRS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,re_path
from django.conf.urls import url,include
from django.views.generic.base import TemplateView
from user import views as v
from user.views import IndexView
from moviedata import views as m
from moviedata.views import detailView,detailbyIDView

urlpatterns = [
    path(r'admin/', admin.site.urls),
    re_path(r'^$', IndexView.as_view(), name=''),
    re_path(r'^search/$', TemplateView.as_view(template_name='search.html'),),
    re_path(r'^search/query$', v.search_detail),
    re_path(r'db$', v.search),
    re_path(r'rating/', v.rating),
    re_path(r'^moviedetail/search$',detailView.as_view(),name=''),
    re_path(r'^moviedetail/searchbyid$',detailbyIDView.as_view(),name=''),
    path(r'accounts/', include('user.url')),
    path(r'accounts/', include('django.contrib.auth.urls')),
    # url(r'accounts/', include('django.contrib.auth.urls')),
]

