from django.shortcuts import render
from .forms import UploadFileForm,ClassPhotoForm
from .models import *
from django.http import HttpResponse
from django.shortcuts import render, redirect
#from supervisors.mixins import SupervisorDomainMixin
from django.views.generic import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, DeleteView
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib import messages
import cloudinary
import cloudinary.uploader
import cloudinary.api
from microsoft import add_person_image,detect_faces
from login.models import Users
from prof.models import Course
from PIL import Image
# Create your views here.

class UploadPhoto(View):
    template_name = 'upload.html'

    def get(self, request):
        print 'Upload a photo'
        form = UploadFileForm()
        return render(request,self.template_name,{'form' : form })

    def post(self, request, **kwargs):
        form = UploadFileForm(request.POST, request.FILES)
        user = request.session['email']
        if form.is_valid():
            print 'valid form'
            name = request.POST['title']
            image = request.FILES['image']
            instance = Photos(name = name, pic= image)
            instance.save()
            print "image saved"
            foo = Image.open(instance.pic.url) 
            (a,b) =  foo.size  
            foo = foo.resize((a/8,b/8),Image.ANTIALIAS)
            foo.save(instance.pic.url)
            response = cloudinary.uploader.upload(instance.pic.url)
            url = response['url']    
            print url
            student = Users.objects.get(email = user, role = 'S')

            add_person_image(student.ID,url)
            # Account creation is successful. Now we need to add the first user
            # to this account. This user will also be the admin of the account.
            return redirect("/student/studenthome/")

        else:
            messages.errors = form.errors
            messages.error(request, 'Invalid fields')
            print messages.errors
            print "Invalid form"

            return HttpResponse("Invalid Form!")

        

class UploadClassPhotos(View):

    template_name = "class_upload.html"

    def get(self, request,course_info):
        print 'Upload a class photo'
        
        form = ClassPhotoForm()
        return render(request,self.template_name,{'form' : form })

    def post(self, request,course_info, **kwargs):
        form = ClassPhotoForm(request.POST, request.FILES)
        info = str(course_info).split(",")
        group_id = str.lower(info[0]) + "_" + str(info[1])
        if form.is_valid():
            print 'valid form'
            course = request.POST['course']
            date = request.POST['date']
            image = request.FILES['image']
            # files = request.FILES.getlist('file_field')
            instance = Photos(name = course, pic= image)
            instance.save()
            print "image saved"
            print instance.pic.url 
            foo = Image.open(instance.pic.url) 
            (a,b) =  foo.size  
            foo = foo.resize((a/8,b/8),Image.ANTIALIAS)
            foo.save(instance.pic.url)
            response = cloudinary.uploader.upload(instance.pic.url)   
            response = cloudinary.uploader.upload(instance.pic.url)
            url = response['url']

            instance = ClassPhoto(course = group_id,date = date, url = url)
            instance.save()    

            detect_faces(info[0],info[1],date,[url])
            course = Course.objects.get(courseID=info[0], year=info[1])
            prof = Users.objects.get(ID=course.profID)

            # Account creation is successful. Now we need to add the first user
            # to this account. This user will also be the admin of the account.
            
            studentList = CourseGroup.objects.filter(person_group_id=(str.lower(str(info[0]))+"_"+str(info[1])))
            try:
                context = {'course': course, 'prof' : prof, 'studentList' : studentList}
                return render(request, 'prof/coursepage.html', context)
            except:
                print "Error"
            return HttpResponse("Error")

        else:
            messages.errors = form.errors
            messages.error(request, 'Invalid fields')
            print messages.errors
            print "Invalid form"

            return HttpResponse("Invalid Form!")


class ChangeProfilePic(View):

    template_name = 'upload.html'

    def get(self, request):
        print 'Change Profile Pic'
        form = UploadFileForm()
        return render(request,self.template_name,{'form' : form })

    def post(self, request, **kwargs):
        form = UploadFileForm(request.POST, request.FILES)
        user = request.session['email']
        if form.is_valid():
            print 'valid form'
            name = request.POST['title']
            image = request.FILES['image']
            name = name+"__profilepic"
            instance = Photos(name = name, pic= image)
            instance.save()
            print "image saved"
            foo = Image.open(instance.pic.url) 
            (a,b) =  foo.size  
            foo = foo.resize((a/8,b/8),Image.ANTIALIAS)
            foo.save(instance.pic.url)
            response = cloudinary.uploader.upload(instance.pic.url)
            url = response['url']    
            print url
            student = Users.objects.get(email = user, role = 'S')
            student.profilePicURL = url
            student.save()
            return redirect("/student/studenthome/")

        else:
            messages.errors = form.errors
            messages.error(request, 'Invalid fields')
            print messages.errors
            print "Invalid form"

            return HttpResponse("Invalid Form!")        



