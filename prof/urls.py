from django.conf.urls import url

from . import views
from photo.views import UploadClassPhotos

urlpatterns = [
    url(r'^homePage/(?P<email_id>[A-Za-z0-9@.]+)/$', views.homePage, name='homePage'),
    url(r'^course/(?P<course_info>[A-Za-z0-9,]+)/$', views.showCourse, name='showCourse'),
    url(r'^addCourse/$',views.AddCourse.as_view(),name='addCourse'),
    url(r'^updateattendance/$',views.UpdateAttendace.as_view(),name='updateattendance'),
    url(r'^viewallqueries/$',views.ViewAllQueries.as_view(),name='viewqueries_prof'),
    url(r'^resolvequery/(?P<query>[A-Za-z0-9,-|]+)/$',views.ResolveQuery.as_view(),name='viewqueries_prof'),
    url(r'^addStudents/(?P<course_info>[A-Za-z0-9,]+)/$',views.AddStudents.as_view(),name='addStudents'),
    url(r'^uploadPhoto/(?P<course_info>[A-Za-z0-9,]+)/$',UploadClassPhotos.as_view(),name='uploadPhoto'),
]