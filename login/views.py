from django.http import HttpResponse
from django.shortcuts import render, redirect
#from supervisors.mixins import SupervisorDomainMixin
from django.views.generic import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, DeleteView
from .forms import UserAddForm
from .models import Users
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib import messages

def index(request):
    return HttpResponse("Welcome to Login Page!.")

class AddUser(View):
	template_name = 'add.html'

	def get(self, request):
		print 'Add an account'
		form = UserAddForm()
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
			return HttpResponse("Added Successfully!")

		else:
			messages.errors = form.errors
			messages.error(request, 'Invalid fields')
			print "Invalid form"

			return HttpResponse("Invalid Form!")

		return redirect("/login/")