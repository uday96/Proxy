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
from ForGreaterGood.settings import MICROSOFT_KEY
import requests
import json
import httplib, urllib, base64
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
            imageList = request.FILES.getlist('image')
            i = 0
            for image in imageList:
                instance = Photos(name = (str(name) + str(i)), pic= image)
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
                i += 1
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
            # image = request.FILES['image']
            imageList = request.FILES.getlist('image')
            urls = []
            image = imageList[0]
            # Add Here =========================================
            # files = request.FILES.getlist('file_field')
            for image in imageList:
                instance = Photos(name = course, pic= image)
                instance.save()
                print "image saved"
                print instance.pic.url 
                foo = Image.open(instance.pic.url) 
                (a,b) =  foo.size  
                foo = foo.resize((a/8,b/8),Image.ANTIALIAS)
                foo.save(instance.pic.url)
                response = cloudinary.uploader.upload(instance.pic.url)   
                #response = cloudinary.uploader.upload(instance.pic.url) # it was there before
                urls.append(response['url'])

                instance = ClassPhoto(course = group_id,date = date, url = response['url'])
                instance.save()    

            detect_faces(info[0],info[1],date,urls)
            course = Course.objects.get(courseID=info[0], year=info[1])
            prof = Users.objects.get(ID=course.profID)

            # Account creation is successful. Now we need to add the first user
            # to this account. This user will also be the admin of the account.
            
            studentList = CourseGroup.objects.filter(person_group_id=(str.lower(str(info[0]))+"_"+str(info[1])))
            try:
                context = {'course': course, 'prof' : prof, 'studentList' : studentList}
                return render(request, 'prof/coursepage.html', context)
            except Exception as e:
                print str(e.message)
            return HttpResponse("Error")

        else:
            messages.errors = form.errors
            messages.error(request, 'Invalid fields')
            print messages.errors
            print "Invalid form"

            return HttpResponse("Invalid Form!")

class DisplayPhotos(View):
    # return HttpResponse("Hello, world. You're at the prof index page.")
    # prof = Users.objects.get(email=email_id)

    template_name = "image_display.html"

    def get(self,request):
        print 'display student photos'
        student_id = "cs14b025"
        urls = []
        ids = []
        versions = []
        try:
            courselist = CourseGroup.objects.filter(student_id=student_id)
            for course in courselist:
                images = PersonPhoto.objects.filter(person_id=course.person_id)
                for image in images:
                    urls.append(image.url)

            urls = list(set(urls))
            for url in urls:
                i = url.split("/")
                versions.append(i[-2])
                ids.append(i[-1])

            data = zip(versions,ids) 
            context = {'studentID' : student_id , 'data' : data}
            print context
            return render(request, self.template_name, context)
            print "here"

        except Exception as e:
            print str(e.message)
            print "error1"

        return HttpResponse("Error1")


def DeletePhoto(request,info):
    print 'deleting student photo'
    data = info.split(",")
    version = data[0]
    img_id = data[1]

    url = "http://res.cloudinary.com/proxy/image/upload/"+version+"/"+img_id
    endpoint = "https://westus.api.cognitive.microsoft.com/face/v1.0/persongroups/"

    headers = {
            "Content-Type":'application/json',
            "Ocp-Apim-Subscription-Key": MICROSOFT_KEY,
    }

    endpoint1 = "https://westus.api.cognitive.microsoft.com/face/v1.0/persongroups/"
    try:
        persons = PersonPhoto.objects.filter(url = url)
        for person in persons:
            print person.person_id
            course = CourseGroup.objects.get(person_id=person.person_id)
            api_url = course.person_group_id+"/persons/"+person.person_id+"/persistedFaces/"+person.persisted_id            
            # print api_url
            # response = requests.request("DELETE",url,data="random",headers=headers)
            
            params = urllib.urlencode({})
          
            try:
                conn = httplib.HTTPSConnection('westus.api.cognitive.microsoft.com')
                conn.request("DELETE", "/face/v1.0/persongroups/"+api_url+"?%s" % params, "{body}", headers)
                response = conn.getresponse()
               
                data = response.read()              
                conn.close()
                print response.status                
                if response.status == 200:
                    print "Successfully deleted from " + course.course_id
                    PersonPhoto.objects.filter(persisted_id=person.persisted_id).delete()

                    url1 = "https://westus.api.cognitive.microsoft.com/face/v1.0/persongroups/"+course.person_group_id+"/train"
                    resp1 = requests.request("POST", url1,data = json.dumps({}) , headers=headers)
                    if resp1.status_code == 202:
                        print "Successfully put for training"
                    else:
                        print "unable to train"
                        print resp1.json()
                else :
                        print response.status
                        print "Error in deleting from " + course.course_id                    
                        print "done"        
                        
            except Exception as e:
                print str(e.message)


    except Exception as e:
        print str(e.message)
        print "Error"

    return redirect('/student/myphotos')


