"""ForGreaterGood URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from login.views import AdminHome, Home, AuthenticatePhotos,authenticate


urlpatterns = [
    url(r'^login/', include('login.urls')),
    url(r'^photo/', include('photo.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^prof/', include('prof.urls')),
    url(r'^student/', include('student.urls')),
    url(r'^attendance/', include('attendance.urls')),
    url(r'^administrator/', AdminHome.as_view(), name="administrator"),
    url(r'^auth/((?P<info>[0-9,]+)$)', authenticate, name="administrator_authenticate"),
    url(r'^authenticate/', AuthenticatePhotos.as_view(), name="authenticate"),
    url(r'^$',Home),
]
