from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^homePage/(?P<email_id>[A-Za-z0-9@.]+)/$', views.homePage, name='homePage'),
    url(r'^course/(?P<course_id>[A-Za-z0-9]+)/$', views.showCourse, name='showCourse'),
    url(r'^addCourse/$',views.AddCourse.as_view(),name='addCourse'),
    url(r'^addStudents/(?P<course_id>[A-Za-z0-9]+)/$',views.AddStudents.as_view(),name='addStudents'),
]