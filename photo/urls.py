from django.conf.urls import url,include
from .views import UploadPhoto,UploadClassPhotos

urlpatterns = [    
    url(r'^upload/',UploadPhoto.as_view(),name='add'),
    url(r'^class_upload/',UploadClassPhotos.as_view(),name='upload')
]
