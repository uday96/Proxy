from django.shortcuts import render
from .forms import UploadFileForm,ClassPhotoForm
from .models import *
from django.http import HttpResponse
from django.shortcuts import render, redirect
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
import logging
from django.db.models import Q
import math

# Get logger
logger = logging.getLogger('backup')

class UploadPhoto(View):

    template_name = 'upload.html'

    def get(self, request):
        logger.info('Upload a photo')
        form = UploadFileForm()
        return render(request,self.template_name,{'form' : form })

    def post(self, request, **kwargs):
        form = UploadFileForm(request.POST, request.FILES)
        user = request.session['email']
        user_instance = Users.objects.get(email=user)
        user_id = user_instance.ID
        if form.is_valid():
            logger.info("["+user+"] Valid Upload Photo Form")
            name = request.POST['title']
            imageList = request.FILES.getlist('image')
            standard_size = 51200

            i = 0
            for image in imageList:
                image_size = image._size
                ratio = image_size/standard_size
                root = math.sqrt(ratio)
                root = int(math.floor(root+0.5))
                logger.info("["+user+"] Saving Image")
                instance = Photos(name = (str(name) + str(i)), pic= image)
                instance.save()
                logger.info("["+user+"] Image Saved")
                foo = Image.open(instance.pic.url)                
                if root != 0:
                    (a,b) =  foo.size  
                    foo = foo.resize((a/root,b/root),Image.ANTIALIAS)
                    foo.save(instance.pic.url)
                    logger.info("Image Resized")

                logger.info("["+user+"] Uploading Image to Cloud")
                response = cloudinary.uploader.upload(instance.pic.url)
                logger.info("["+user+"] Uploaded Image to Cloud Successfully!")
                url = response['url']    
                logger.debug("Url: "+str(url))
                new_photo = StudentPhotos(studentID=user_id,url=url,status='P')
                new_photo.save()
                # student = Users.objects.get(email = user, role = 'S')
                # add_person_image(student.ID,url)
                i += 1
            return redirect("/student/studenthome/")
        else:
            logger.error("Invalid Upload Photo Form")
            return HttpResponse("Invalid Form!")

        

class UploadClassPhotos(View):

    template_name = "class_upload.html"

    def get(self, request,course_info):
        logger.info('Upload a class photo')        
        form = ClassPhotoForm()
        return render(request,self.template_name,{'form' : form })

    def post(self, request,course_info, **kwargs):
        form = ClassPhotoForm(request.POST, request.FILES)
        info = str(course_info).split(",")
        group_id = str.lower(info[0]) + "_" + str(info[1])
        if form.is_valid():
            logger.info('Valid Upload Class Photo Form')
            course = request.POST['course']
            date = request.POST['date']
            imageList = request.FILES.getlist('image')
            urls = []
            image = imageList[0]
            standard_size = 51200
            # files = request.FILES.getlist('file_field')
            for image in imageList:
                image_size = image._size
                ratio = image_size/standard_size
                root = math.sqrt(ratio)
                root = int(math.floor(root+0.5))
                instance = Photos(name = course, pic= image)
                instance.save()
                logger.info("Image Saved")
                logger.debug("Url: "+str(instance.pic.url))
                foo = Image.open(instance.pic.url) 

                if root != 0:
                    (a,b) =  foo.size  
                    foo = foo.resize((a/root,b/root),Image.ANTIALIAS)
                    foo.save(instance.pic.url)
                    logger.info("Image Resized")                
                
                logger.info("Uploading Image to Cloud")
                response = cloudinary.uploader.upload(instance.pic.url)
                logger.info("Uploaded Image to Cloud Successfully!")
                urls.append(response['url'])
                instance = ClassPhoto(course = group_id,date = date, url = response['url'])
                instance.save()
                logger.info("Class Photo Saved")    

            detect_faces(info[0],info[1],date,urls)
            course = Course.objects.get(courseID=info[0], year=info[1])
            prof = Users.objects.get(ID=course.profID)
            
            studentList = CourseGroup.objects.filter(person_group_id=(str.lower(str(info[0]))+"_"+str(info[1])))
            try:
                context = {'course': course, 'prof' : prof, 'studentList' : studentList}
                return render(request, 'coursepage.html', context)
            except Exception as e:
                logger.error(str(e))
            return HttpResponse("Error")

        else:
            logger.error("Invalid Upload Class Photo Form")
            return HttpResponse("Invalid Form!")


class ChangeProfilePic(View):

    template_name = 'upload.html'

    def get(self, request):
        logger.info('Change Profile Pic')
        form = UploadFileForm()
        return render(request,self.template_name,{'form' : form })

    def post(self, request, **kwargs):
        form = UploadFileForm(request.POST, request.FILES)
        user = request.session['email']
        if form.is_valid():
            logger.info("["+user+"] Valid Change Profile Pic Form")
            name = request.POST['title']
            image = request.FILES['image']
            name = name+"__profilepic"
            logger.info("["+user+"] Saving Image")
            instance = Photos(name = name, pic= image)
            instance.save()
            logger.info("["+user+"] Image Saved")
            foo = Image.open(instance.pic.url) 
            (a,b) =  foo.size  
            foo = foo.resize((a/8,b/8),Image.ANTIALIAS)
            foo.save(instance.pic.url)
            logger.info("["+user+"] Image Resized")
            logger.info("["+user+"] Uploading Image to Cloud")
            response = cloudinary.uploader.upload(instance.pic.url)
            url = response['url']    
            logger.debug("Url: "+str(url))
            student = Users.objects.get(email = user, role = 'S')
            student.profilePicURL = url
            student.save()
            logger.info("["+user+"] Updated Profile Pic Url")
            return redirect("/student/studenthome/")

        else:
            logger.error("Invalid Change Profile Pic Form")
            return HttpResponse("Invalid Form!")        


class DisplayPhotos(View):

    template_name = "image_display.html"

    def get(self,request):
        logger.info('Display Student Photos')
        user = request.session['email']
        user = Users.objects.get(email=user)
        student_id = user.ID
        logger.info("student is " + student_id)
        urls = []
        pend_urls = []
        ids = []
        versions = []
        pend_ids = []
        pend_versions = []
        try:
            # courselist = CourseGroup.objects.filter(student_id=student_id)
            # for course in courselist:
            images = StudentPhotos.objects.filter(studentID=student_id,status='A')
            pend_images = StudentPhotos.objects.filter(studentID=student_id,status='P')
            for image in images:
                urls.append(image.url)

            for image in pend_images:
                pend_urls.append(image.url)

            urls = list(set(urls))
            pend_urls = list(set(pend_urls))
            for url in urls:
                i = url.split("/")
                versions.append(i[-2])
                ids.append(i[-1])

            for url in pend_urls:
                i = url.split("/")
                pend_versions.append(i[-2])
                pend_ids.append(i[-1])

            data = zip(versions,ids) 
            pend_data = zip(pend_versions,pend_ids)
            context = {'studentID' : student_id , 'data' : data,'pend_data':pend_data}
            
            return render(request, self.template_name, context)
           

        except Exception as e:
            logger.error(str(e.message))
            logger.error("error in deleting photos")

        return HttpResponse("Error1")


def DeletePhoto(request,info):
    logger.info('Deleting Student Photo')
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
            logger.debug("Person: "+str(person.person_id))
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
                logger.debug("Status: "+str(response.status))
                if response.status == 200:
                    logger.info("Successfully deleted from " + str(course.course_id))
                    PersonPhoto.objects.filter(persisted_id=person.persisted_id).delete()
                    StudentPhotos.objects.filter(url=url).delete()
                    url1 = "https://westus.api.cognitive.microsoft.com/face/v1.0/persongroups/"+course.person_group_id+"/train"
                    resp1 = requests.request("POST", url1,data = json.dumps({}) , headers=headers)
                    if resp1.status_code == 202:
                        logger.info("Successfully put for Training")
                    else:
                        logger.info("Unable to Train")
                        logger.debug(str(resp1.json()))
                else:
                    logger.error("Error in deleting from " + str(course.course_id))
                    logger.info("Done")
            except Exception as e:
                logger.error(str(e))
    except Exception as e:
        logger.error(str(e))
    return redirect('/student/myphotos')