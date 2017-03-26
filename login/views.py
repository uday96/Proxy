from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, DeleteView
from .forms import UserAddForm, UserLoginForm
from .models import Users
from .functions import check_password
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib import messages
import cloudinary
import cloudinary.uploader
import cloudinary.api
from pymsgbox import *

def Home(request):
	print "Home Page!"
	return redirect("/login/")


class Logout(View):

	def get(self,request):
		if 'email' in request.session:
			del request.session['email']
			request.session.modified = True
		return redirect("/login/")

class LoginHome(View):
	template_name = 'index.html'

	def get(self, request):
		print 'Login get'
		form = UserLoginForm()
		return render(request,self.template_name,{'header' : "Login",'form' : form })

	def post(self, request, **kwargs):
		print 'Login post'
		form = UserLoginForm(request.POST)
		if form.is_valid():
			print 'valid form'
			mail = form.cleaned_data['email']
			password = form.cleaned_data['password']
			isnewuser = form.cleaned_data['newuser']
			if(isnewuser == True):
				print "newuser"
				return redirect("add?mail="+mail)
			else:
				print "existing user"
				userob = Users.objects.get(email=mail)
				if(check_password(password,userob.password)==True):
					print "Password Match"
					request.session['email'] = mail
					if userob.role == "T":
						return redirect("/prof/homePage/"+mail)	
					else:
						return redirect("/student/studenthome?mail="+mail)		
					return HttpResponse("Login Successful")
				print "Password Mismatch"
				return redirect("/login/")	
			

class AddUser(View):
	template_name = 'index.html'

	def get(self, request):
		print 'Add an account'
		mail = ""
		if(request.GET['mail'] != None):
			mail = request.GET['mail']
		form = UserAddForm(initial={'email' : mail})
		return render(request,self.template_name,{'header' : "Add User",'form' : form })

	def post(self, request, **kwargs):
		form = UserAddForm(request.POST)
		if form.is_valid():
			print 'valid form'
			name = form.cleaned_data['name']
			email = form.cleaned_data['email']
			ID = form.cleaned_data['ID']
			deptID = form.cleaned_data['deptID']
			role = form.cleaned_data['role']
			password = form.cleaned_data['password']
			print "role : "+role
			try:
				print "Adding User"
				user = Users.objects.create(
					name = name,
					email = email,
					ID = ID,
					deptID = deptID,
					role = role,
					password = password,
				)
				user.save()
				#alert(text='User Created Successfully!', title='Status', button='OK')
			except IntegrityError:
				messages.errors = "User already Exists"
				messages.error(request, 'User already Exists')
				return redirect("/login/")

			# Account creation is successful. Now we need to add the first user
			# to this account. This user will also be the admin of the account.
			return redirect("/login/")

		else:
			messages.errors = form.errors
			messages.error(request, 'Invalid fields')
			print "Invalid form"

			return HttpResponse("Invalid Form!")

		return redirect("/login/")