from django.conf.urls import url,include
from . import views

urlpatterns = [    
    url(r'^upload/',views.UploadPhoto.as_view(),name='add'),
    url(r'^class_upload/',views.UploadClassPhotos.as_view(),name='upload'),
    url(r'^changeDP/',views.ChangeProfilePic.as_view(),name='DP'),
]
