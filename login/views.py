from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, DeleteView
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

	template_name = 'index.html'

	def get(self, request):
		logger.info("Logging In")
		form = UserLoginForm()
		return render(request,self.template_name,{'header' : "Login",'form' : form })

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
					if userob.role == "T":
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

	template_name = 'index.html'

	def get(self, request):
		logger.info('Add an account')
		mail = ""
		if(request.GET.get('mail',None) != None):
			mail = request.GET['mail']
		form = UserAddForm(initial={'email' : mail})
		return render(request,self.template_name,{'header' : "Add User",'form' : form })

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
				return redirect("/login/")
			return redirect("/login/")
		else:
			logger.error("Invalid AddUser Form")
			return HttpResponse("Invalid Form!")
		return redirect("/login/")

class ForgotPwd(View):

	template_name = 'index.html'

	def get(self, request):
		logger.info('Forgot Pwd')
		mail = ""
		if(request.GET.get('mail',None) != None):
			mail = request.GET['mail']
		form = UserAddForm(initial={'email' : mail})
		return render(request,self.template_name,{'header' : "Forgot Password",'form' : form })

	def post(self, request, **kwargs):
		form = UserAddForm(request.POST)
		if form.is_valid():
			logger.info("Valid Change Pwd Form")
			name = form.cleaned_data['name']
			email = form.cleaned_data['email']
			ID = form.cleaned_data['ID']
			deptID = form.cleaned_data['deptID']
			role = form.cleaned_data['role']
			password = form.cleaned_data['password']
			try:
				logger.info("["+email+"] Retrieving User")
				logger.debug("Role : "+role)
				existing_user = Users.objects.get(
					name = name,
					email = email,
					ID = ID,
					deptID = deptID,
					role = role
				)
				logger.info("["+email+"] Updating Pwd")
				newPassword = set_password(password)
				existing_user.password = newPassword
				existing_user.save()
				logger.info("["+email+"] Updated Pwd Successfully!")
			except Exception as e:
				logger.error("["+email+"] Change Pwd Failed : "+str(e))
				return redirect("/login/")
			# Change pwd is successful.
			return redirect("/login/")
		else:
			logger.error("Invalid Change Pwd Form")
			return HttpResponse("Invalid Form!")
		return redirect("/login/")