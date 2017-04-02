from django.conf.urls import url
from . import views
from photo.views import DisplayPhotos,DeletePhoto

urlpatterns = [
    url(r'^studenthome/', views.StudentHome.as_view(), name='studenthome'),
    url(r'^raisequery/', views.RaiseQuery.as_view(), name='raiseQuery'),
    url(r'^viewqueries/', views.ViewQueries.as_view(), name='viewQueries'),
    url(r'^deletephoto/((?P<info>[A-Za-z0-9.,]+)/$)', DeletePhoto, name='DeletePhoto'),
    url(r'^myphotos/', DisplayPhotos.as_view(), name='viewPhotos'),


]