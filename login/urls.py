from django.conf.urls import url,include
from .views import AddUser,LoginHome

urlpatterns = [
    url(r'^$',LoginHome.as_view(),name='login'),
    url(r'^add/',AddUser.as_view(),name='add'),
]