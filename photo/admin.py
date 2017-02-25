from django.contrib import admin

# Register your models here.
from .models import Photos,StudentPhoto,ClassPhoto,PersonPhoto,CourseGroup
# Register your models here.

admin.site.register(Photos)
admin.site.register(StudentPhoto)
admin.site.register(ClassPhoto)
admin.site.register(CourseGroup)
admin.site.register(PersonPhoto)