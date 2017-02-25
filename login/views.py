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

class LoginHome(View):
	template_name = 'add.html'

	def get(self, request):
		print 'Login get'
		form = UserLoginForm()
		return render(request,self.template_name,{'form' : form })

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
					return HttpResponse("Login Successful")
				print "Password Mismatch"
				return redirect("/login/")	
			

class AddUser(View):
	template_name = 'add.html'

	def get(self, request):
		print 'Add an account'
		mail = ""
		if(request.GET['mail'] != None):
			mail = request.GET['mail']
		form = UserAddForm(initial={'email' : mail})
		return render(request,self.template_name,{'form' : form })

	def post(self, request, **kwargs):
		form = UserAddForm(request.POST)
		if form.is_valid():
			print 'valid form'
			name = form.cleaned_data['name']
			email = form.cleaned_data['email']
			role = form.cleaned_data['role']
			password = form.cleaned_data['password']

			try:
				print "Adding User"
				user = Users.objects.create(
					name = name,
					email = email,
					role = role,
					password = password,
				)
				user.save()

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