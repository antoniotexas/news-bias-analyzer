from django.conf.urls import url
from django.contrib import admin
from .views import HomeView, ChartData

#FOR SEARCH STUFF
#urlpatterns = [
    #url(r'^$', views.index, name='index'),
    #url(r'^new/$', views.search_new, name='search_new'),
#]

#in searh folder
#FOR GRAPH STUF
urlpatterns = [
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^api/chart/data/', ChartData.as_view()),
]
