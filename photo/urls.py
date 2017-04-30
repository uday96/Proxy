from django.conf.urls import url,include
from . import views

urlpatterns = [    
    url(r'^upload/',views.UploadPhoto.as_view(),name='add'),
    url(r'^class_upload/',views.UploadClassPhotos.as_view(),name='upload'),
    url(r'^changeDP/',views.ChangeProfilePic.as_view(),name='DP'),
    url(r'^finalise_attendance/',views.finalise.as_view(),name='finalise_attendance'),
    url(r'^change_attendance/',views.changeAttendance.as_view(),name='change_attendance'),
]
