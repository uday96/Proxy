from django.shortcuts import render
from .forms import UploadFileForm,ClassPhotoForm
from .models import Photos,StudentPhoto,ClassPhoto
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
			print instance.pic.url	
			response = cloudinary.uploader.upload(instance.pic.url)
			url = response['url']	
			student = Users.objects.get(email = user, role = 'S')
			add_person_image(student.ID,url)
			# Account creation is successful. Now we need to add the first user
			# to this account. This user will also be the admin of the account.
			return HttpResponse("Added Successfully!")

		else:
			messages.errors = form.errors
			messages.error(request, 'Invalid fields')
			print messages.errors
			print "Invalid form"

			return HttpResponse("Invalid Form!")

		return redirect("/login/")

class UploadClassPhotos(View):

	template_name = "class_upload.html"

	def get(self, request,course_info):
		print 'Upload a class photo'
		
		form = ClassPhotoForm()
		return render(request,self.template_name,{'form' : form })

	def post(self, request,course_info, **kwargs):
		form = ClassPhotoForm(request.POST, request.FILES)
		info = str(course_info).split(",")
		course_name = str.lower(info[0]) + "_" + str(info[1])
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
			response = cloudinary.uploader.upload(instance.pic.url)
			url = response['url']

			instance = ClassPhoto(course = course_name,date = date, url = url)
			instance.save()	

			detect_faces(info[0],info[1],date,[url])

			# Account creation is successful. Now we need to add the first user
			# to this account. This user will also be the admin of the account.
			return HttpResponse("Added Successfully!")

		else:
			messages.errors = form.errors
			messages.error(request, 'Invalid fields')
			print messages.errors
			print "Invalid form"

			return HttpResponse("Invalid Form!")

		return redirect("/login/")



