from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^studenthome/', views.StudentHome.as_view(), name='studenthome'),
    url(r'^raisequery/', views.RaiseQuery.as_view(), name='raiseQuery'),
    url(r'^viewqueries/', views.ViewQueries.as_view(), name='viewQueries'),
]