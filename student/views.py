from django.shortcuts import render, redirect
from django.views.generic import View
from login.models import Users
from django.http import HttpResponse
from .forms import RaiseQueryForm
from .models import Queries
from photo.models import CourseGroup
from pymsgbox import *

# Create your views here.
class StudentHome(View):
	
	template_name = "studenthome.html"

	def get(self,request):
		email = request.GET.get('mail',None)
		email = request.session['email'] if 'email' in request.session else email
		if not email:
			print "Error"
			return HttpResponse("Error")
		
		student = Users.objects.get(email=email,role="S")
		courselist = CourseGroup.objects.filter(student_id = student.ID)
		print courselist
		try:
			context = {'student' : student,'course_list':courselist}
			print context
			return render(request,self.template_name,context)
		except:
			print "Error"
		return HttpResponse("Error")

class RaiseQuery(View):
	
	template_name = "raisequery.html"

	def get(self,request):
		print "raisequery get"
		email = request.session['email'] if 'email' in request.session else None
		if not email:
			print "Error"
			return HttpResponse("Error")
		student = Users.objects.get(email=email,role="S")
		form = RaiseQueryForm(initial={'studentID':student.ID})
		return render(request,self.template_name,{'form' : form })

	def post(self, request, **kwargs):
		print 'raisequery post'
		form = RaiseQueryForm(request.POST)
		if form.is_valid():
			print 'valid form'
			studentID = form.cleaned_data['studentID']
			courseID = form.cleaned_data['courseID']
			query = form.cleaned_data['query']
			try:
				queryraised = Queries.objects.create(studentID=studentID,courseID=courseID,query=query)
				print queryraised.date
				queryraised.save()
				alert(text='Query Raised Successfully!', title='Status', button='OK')
				return redirect("/student/studenthome/")
			except:
				print "Error"
			return HttpResponse("Error")
		return HttpResponse("Error")


class ViewQueries(View):
	
	template_name = "viewqueries.html"

	def get(self,request):
		print "viewqueries get"
		email = request.GET.get('mail',None)
		email = request.session['email'] if 'email' in request.session else email
		if not email:
			print "Error"
			return HttpResponse("Error")
		try:
			student = Users.objects.get(email=email,role="S")
			studentID = student.ID
			allqueries = Queries.objects.filter(studentID=studentID)
			return render(request,self.template_name,{'studentID' : studentID ,'query_list' : allqueries })
		except:
			print "Error"
		return HttpResponse("Error")