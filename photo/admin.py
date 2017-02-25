from django.contrib import admin

# Register your models here.
from .models import Photos,StudentPhoto,ClassPhoto
# Register your models here.

admin.site.register(Photos)
admin.site.register(StudentPhoto)
admin.site.register(ClassPhoto)