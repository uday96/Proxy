from django.conf.urls import url,include
from .views import index,AddUser

urlpatterns = [
    url(r'^$',index,name='index'),
    url(r'^add/',AddUser.as_view(),name='add'),
]