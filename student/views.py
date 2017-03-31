from django.shortcuts import render, redirect
from django.views.generic import View
from login.models import Users
from django.http import HttpResponse
from .forms import RaiseQueryForm
from .models import Queries
from photo.models import CourseGroup
from pymsgbox import *
from django.utils.decorators import method_decorator
from functools import wraps

# Create your views here.

#Decorator Functions
def assess_role_stud(view_func):
    def _decorator(request):
        if ('email' not in request.session) or ('role' not in request.session):
            return redirect("/login/logout/")
        elif request.session.get('role',"")!='S':
            return redirect("/login/logout/")
        else:
            response = view_func(request)
        return response
    return wraps(view_func)(_decorator)

class StudentHome(View):

	template_name = "studenthome.html"

	@method_decorator(assess_role_stud)
	def dispatch(self, request):
		return super(StudentHome, self).dispatch(request)

	def get(self,request):
		email_get = request.GET.get('mail',None)
		email = request.session.get('email',email_get)
		if not email:
			print "Error"
			return HttpResponse("Error")
		
		try:
			student = Users.objects.get(email=email,role="S")
			courselist = CourseGroup.objects.filter(student_id = student.ID)
			print courselist
			context = {'student' : student,'course_list':courselist}
			print context
			return render(request,self.template_name,context)
		except:
			print "Error"
		return HttpResponse("Error")

class RaiseQuery(View):
	
	template_name = "raisequery.html"

	@method_decorator(assess_role_stud)
	def dispatch(self, request):
		return super(RaiseQuery, self).dispatch(request)

	def get(self,request):
		print "raisequery get"
		email = request.session.get('email',None)
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
				#alert(text='Query Raised Successfully!', title='Status', button='OK')
				return redirect("/student/studenthome/")
			except:
				print "Error"
			return HttpResponse("Error")
		return HttpResponse("Error")


class ViewQueries(View):
	
	template_name = "viewqueries.html"

	@method_decorator(assess_role_stud)
	def dispatch(self, request):
		return super(ViewQueries, self).dispatch(request)

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