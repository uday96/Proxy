from django.conf.urls import url,include
from . import views

urlpatterns = [
    url(r'^$',views.LoginHome.as_view(),name='login'),
    url(r'^add/',views.AddUser.as_view(),name='add'),
    url(r'^forgot/',views.ForgotPwd.as_view(),name='forgot'),
    url(r'^logout/',views.Logout.as_view(),name='logout'),
]