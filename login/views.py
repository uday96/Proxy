from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import View
from .forms import UserAddForm, UserLoginForm
from .models import Users
from .functions import check_password, set_password
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib import messages
import cloudinary
import cloudinary.uploader
import cloudinary.api
from pymsgbox import *
from django.core.exceptions import ObjectDoesNotExist
import logging
from django.views.decorators.csrf import csrf_exempt
from photo.models import StudentPhotos
from photo.microsoft import add_person_image


#Get Logger
logger = logging.getLogger('backup')

def Home(request):
	print "Home Page!"
	return redirect("/login/")


class Logout(View):

	def get(self,request):
		print "Logout get"
		if 'email' in request.session:
			email = request.session['email']  
			logger.info("["+email+"] Logged Out Successfully!")
			del request.session['email']
			request.session.modified = True
		if 'role' in request.session:
			del request.session['role']
			request.session.modified = True
		return redirect("/login/")

class LoginHome(View):

	template_name = 'login.html'

	def get(self, request):
		logger.info("Logging In")
		form = UserLoginForm()
		return render(request,self.template_name,{'header' : "Login",'form' : form })

	@csrf_exempt
	def post(self, request, **kwargs):
		print 'Login post'
		form = UserLoginForm(request.POST)
		if form.is_valid():
			logger.info("Valid Login Form")
			mail = form.cleaned_data['email']
			password = form.cleaned_data['password']
			try:
				userob = Users.objects.get(email=mail)
				logger.info("Existing User")
				if(check_password(password,userob.password)==True):
					logger.info("Password Match")
					request.session['email'] = mail
					request.session['role'] = userob.role
					logger.info("Session Variables Updated")
					logger.info("Logged In Successfully!")
					if userob.role == "A":
						return redirect("/administrator/")
					elif userob.role == "T":
						return redirect("/prof/profhome/")
					else:
						return redirect("/student/studenthome/")		
					return HttpResponse("Login Successful")
				logger.error("Password Mismatch")
				return redirect("/login/")
			except ObjectDoesNotExist:
				logger.error("No User Record Found")
				return redirect("/login/add/")
		else:
			logger.error("Invalid Form")
			return redirect("/login/")
			

class AddUser(View):

	template_name = 'newUser.html'

	def get(self, request):
		logger.info('Add an account')
		return render(request,self.template_name)

	@csrf_exempt
	def post(self, request, **kwargs):
		form = UserAddForm(request.POST)
		if form.is_valid():
			logger.info("Valid AddUser Form")
			name = form.cleaned_data['name']
			email = form.cleaned_data['email']
			ID = form.cleaned_data['ID']
			deptID = form.cleaned_data['deptID']
			role = form.cleaned_data['role']
			password = form.cleaned_data['password']
			try:
				logger.info("Adding User ["+email+"]")
				logger.debug("Role : "+role)
				user = Users.objects.create(
					name = name,
					email = email,
					ID = ID,
					deptID = deptID,
					role = role,
					password = password,
				)
				user.save()
				logger.info("User ["+email+"] Added Successfully!")
				#alert(text='User Created Successfully!', title='Status', button='OK')
			except IntegrityError:
				logger.error("User ["+email+"] Already Exists!")
				return redirect("/administrator/")
			return redirect("/administrator/")
		else:
			logger.error("Invalid AddUser Form")
			return HttpResponse("Invalid Form!")
		return redirect("/administrator/")

class ForgotPwd(View):

	template_name = 'password.html'

	def get(self, request):
		logger.info('Forgot Pwd')
		return render(request,self.template_name)

	@csrf_exempt
	def post(self, request, **kwargs):
		form = UserLoginForm(request.POST)
		if form.is_valid():
			logger.info("Valid Change Pwd Form")
			email = form.cleaned_data['email']
			password = form.cleaned_data['password']
			try:
				logger.info("["+email+"] Retrieving User")
				existing_user = Users.objects.get(email = email)
				logger.info("["+email+"] Updating Pwd")
				newPassword = set_password(password)
				existing_user.password = newPassword
				existing_user.save()
				logger.info("["+email+"] Updated Pwd Successfully!")
			except Exception as e:
				logger.error("["+email+"] Change Pwd Failed : "+str(e))
				return redirect("/administrator/")
			# Change pwd is successful.
			return redirect("/administrator/")
		else:
			logger.error("Invalid Change Pwd Form")
			return HttpResponse("Invalid Form!")
		return redirect("/administrator/")

class AdminHome(View):

	template_name = "adminhome.html"

	def get(self,request):
		email = request.session['email']		
		try:
			logger.info("["+email+"] Retrieving Admin Info")
			admin = Users.objects.get(email=email,role="A")
			context = {'admin' : admin}
			logger.info("["+email+"] Retrieved Admin Info Successfully")
			return render(request,self.template_name,context)
		except Exception as e:
			logger.error("["+email+"] "+str(e))
		return HttpResponse("Error")

@csrf_exempt
def authenticate(request,info):
	logger.info("information got is " + info)
	data = info.split(",")
	row_id = int(data[0])
	action = int(data[1])

	instance = StudentPhotos.objects.get(id=row_id)
	url = instance.url
	student_id = instance.studentID

	if action == 0:
		instance.status = 'R'
		instance.save()
	else:
		add_person_image(student_id,url,instance)

	return redirect('/authenticate/')


class AuthenticatePhotos(View):

	template_name = "authenticate.html"

	def get(self,request):
		logger.info("[admin] Authenticating Photos")
		try:
			toAuthenticate = StudentPhotos.objects.filter(status="P")
			PhotosInfo = []
			for StudentPhoto in toAuthenticate:
				studentID = StudentPhoto.studentID
				student = Users.objects.get(ID=studentID,role="S")
				profilePicURL = student.profilePicURL
				StudentPhotoInfo = StudentPhoto.__dict__
				StudentPhotoInfo["profilePicURL"] = profilePicURL
				ID = StudentPhoto.id
				StudentPhotoInfo["ID"] = ID	
				PhotosInfo.append(StudentPhotoInfo)
			context = {"Photos": PhotosInfo}
			return render(request,self.template_name,context)
		except Exception as e:
			logger.error("[admin] "+str(e))

