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
import logging

# Get logger
logger = logging.getLogger('backup')

#Decorator Functions
def assess_role_stud(view_func):
    def _decorator(request):
        if ('email' not in request.session) or ('role' not in request.session):
        	logger.error("Invalid Session")
        	return redirect("/login/logout/")
        elif request.session.get('role',"")!='S':
        	logger.error("Invalid Session")
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
		email = request.session['email']		
		try:
			logger.info("["+email+"] Retrieving Student Info")
			student = Users.objects.get(email=email,role="S")
			courselist = CourseGroup.objects.filter(student_id = student.ID)
			logger.debug("CourseList: "+str(courselist))
			context = {'student' : student,'course_list':courselist}
			logger.info("["+email+"] Retrieved Student Info Successfully")
			return render(request,self.template_name,context)
		except Exception as e:
			logger.error("["+email+"]"+str(e))
		return HttpResponse("Error")

class RaiseQuery(View):
	
	template_name = "raisequery.html"

	@method_decorator(assess_role_stud)
	def dispatch(self, request):
		return super(RaiseQuery, self).dispatch(request)

	def get(self,request):
		print "raisequery get"
		email = request.session['email']
		logger.info("["+email+"]"+" Raising Query")
		student = Users.objects.get(email=email,role="S")
		logger.info("["+email+"]"+" User object retrieved")
		form = RaiseQueryForm(initial={'studentID':student.ID})
		return render(request,self.template_name,{'form' : form })

	def post(self, request, **kwargs):
		print 'raisequery post'
		form = RaiseQueryForm(request.POST)
		email = request.session["email"]
		if form.is_valid():
			logger.info("["+email+"]"+" Raise Query-Valid Form")
			studentID = form.cleaned_data['studentID']
			courseID = form.cleaned_data['courseID']
			query = form.cleaned_data['query']
			try:
				queryraised = Queries.objects.create(studentID=studentID,courseID=courseID,query=query)
				logger.debug("date: "+str(queryraised.date))
				queryraised.save()
				#alert(text='Query Raised Successfully!', title='Status', button='OK')
				logger.info("["+email+"]"+"Query Raised Successfully!")
				return redirect("/student/studenthome/")
			except Exception as e:
				logger.error("["+email+"]"+str(e))
			return HttpResponse("Error")
		logger.error("["+email+"] Invalid Form")
		return HttpResponse("Error")


class ViewQueries(View):
	
	template_name = "viewqueries.html"

	@method_decorator(assess_role_stud)
	def dispatch(self, request):
		return super(ViewQueries, self).dispatch(request)

	def get(self,request):
		print "viewqueries get"
		email = request.session['email']
		logger.info("["+email+"] Viewing Queries")
		try:
			student = Users.objects.get(email=email,role="S")
			studentID = student.ID
			allqueries = Queries.objects.filter(studentID=studentID)
			logger.info("["+email+"] Queries Retrieved")
			return render(request,self.template_name,{'studentID' : studentID ,'query_list' : allqueries })
		except Exception as e:
			logger.error("["+email+"]"+str(e))
		return HttpResponse("Error")