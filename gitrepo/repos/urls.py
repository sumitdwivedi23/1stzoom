from django.conf.urls import url
from repos.views import Fetch, devs
from django.urls import path

app_name = 'repos'

urlpatterns = [
    url("trends",Fetch.as_view(),name="tren"),
    url("devs",devs.as_view(),name="devs"),

    
]