from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^course/(?P<course_id>[A-Za-z0-9]+)/$', views.showCourse, name='showCourse'),
]