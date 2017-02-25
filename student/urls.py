from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^studenthome/', views.StudentHome.as_view(), name='studenthome'),
]