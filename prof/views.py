from django.shortcuts import render, redirect
from django.views.generic import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, DeleteView
from django.http import HttpResponse
from .models import Course
from login.models import Users
from student.models import Queries
from attendance.models import Attendance
from .forms import CourseAddForm, StudentAddForm, UpdateAttendanceForm
from photo.microsoft import create_person,create_person_group
import datetime
from photo.models import CourseGroup
from pymsgbox import *
from django.utils.decorators import method_decorator
from functools import wraps
import logging

# Get logger
logger = logging.getLogger('backup')


#Decorator Functions
def assess_role_prof(view_func):
    def _decorator(request):
        if ('email' not in request.session) or ('role' not in request.session):
            logger.error("Invalid Session")
            return redirect("/login/logout/")
        elif request.session.get('role',"")!='T':
            logger.error("Invalid Session")
            return redirect("/login/logout/")
        else:
            response = view_func(request)
        return response
    return wraps(view_func)(_decorator)


class AddCourse(View):

    template_name = 'add.html'

    @method_decorator(assess_role_prof)
    def dispatch(self, request):
        return super(AddCourse, self).dispatch(request)

    def get(self, request):
        print 'AddCourse get'
        email = request.session['email']  
        logger.info("["+email+"] Adding Course")
        form = CourseAddForm()
        prof = Users.objects.get(email=email,role="T")
        return render(request,self.template_name,{'header' : "Add Course",'form' : form,'prof':prof })

    def post(self, request, **kwargs):
        print 'AddCourse post'
        form = CourseAddForm(request.POST)
        profEmail = request.session['email']
        if form.is_valid():
            logger.info("["+profEmail+"] AddCourse Valid Form")
            name = form.cleaned_data['name']
            courseID = form.cleaned_data['courseID']
            year = form.cleaned_data['year']
            room = form.cleaned_data['room']
            logger.info("["+profEmail+"] Retrieved Form Data")
            logger.info("["+profEmail+"] Retrieving User Object")
            prof = Users.objects.get(email=profEmail)
            logger.info("["+profEmail+"] Retrieved User Object")
            logger.info("["+profEmail+"] Creating Person Group")
            create_person_group(profEmail,courseID,year)
            logger.info("["+profEmail+"] Created Person Group Successfully!")
            logger.info("["+profEmail+"] Creating Course Instance")
            instance = Course(courseID=courseID, year=year, deptID=prof.deptID, name=name, room=room, profID=prof.ID)
            instance.save()
            logger.info("["+profEmail+"] Course Instance Saved Successfully!")
            #alert(text='Course Created Successfully!', title='Status', button='OK')
            try:
                courseList = Course.objects.filter(profID=prof.ID)
                context = {'course_list': courseList, 'prof' : prof}
                return render(request, 'homepage.html', context)
            except:
                logger.error("["+profEmail+"] Failed to retrieve Course List")
            return HttpResponse("Error")
            # Call the function to create PersonGroup Microsoft API
            # return HttpResponse("courseID, year, profID: " + str(courseID) + "," + str(year) + "," + str(prof.ID))
        else:
            logger.error("["+profEmail+"] Invalid Form")
            return HttpResponse("Error")

class AddStudents(View):

    template_name = 'add.html'

    def get(self, request, course_info):
        print 'AddStudents get'
        email = request.session['email']  
        logger.info("["+email+"] Adding Students")
        form = StudentAddForm()
        prof = Users.objects.get(email=email,role="T")
        return render(request,self.template_name,{'header' : "Add Student",'form' : form, 'prof': prof })

    def post(self, request, course_info, **kwargs):
        print 'AddStudents post'
        form = StudentAddForm(request.POST)
        profEmail = request.session['email']
        if form.is_valid():
            logger.info("["+profEmail+"] AddStudents Valid Form")
            logger.info("["+profEmail+"] Retrieving User Object")
            prof = Users.objects.get(email=profEmail)
            logger.info("["+profEmail+"] Retrieved User Object")
            studentIDs = str(form.cleaned_data['studentIDs']).split(',')
            [course_id, year] = str(course_info).split(',')
            logger.info("["+profEmail+"] Creating Persons")
            create_person(course_id,year,studentIDs)
            logger.info("["+profEmail+"] Created Persons Successfully!")
            # alert('Success')
            # alert(text='', title='', button='OK')
            # print request.POST
            # Call the function to create PersonGroup Microsoft API
            try:
                course = Course.objects.get(courseID=course_id, year=year)
                studentList = CourseGroup.objects.filter(person_group_id=(str.lower(str(course_id))+"_"+str(year)))
                context = {'course': course, 'prof' : prof, 'studentList' : studentList}
                return render(request, 'coursepage.html', context)
            except Exception as e:
                logger.error("["+profEmail+"] "+str(e))
            return HttpResponse("Error")
            # return HttpResponse("courseID, studentIDs, profID: " + str(course_id) + "," + str(studentIDs) + "," + str(prof.ID))
        else:
            logger.error("["+profEmail+"] Invalid Form")
            return HttpResponse("Error")
            

class ProfHome(View):

    template_name = 'homepage.html'

    @method_decorator(assess_role_prof)
    def dispatch(self, request):
        return super(ProfHome, self).dispatch(request)

    def get(self,request):
        print "profhome get"
        email = request.session.get('email',None)
        try:
            logger.info("["+email+"] Retrieving Prof Info")
            prof = Users.objects.get(email=email,role='T')
            courseList = Course.objects.filter(profID=prof.ID)
            logger.info("["+email+"] Retrieved Prof Info Successfully!")
            context = {'course_list': courseList, 'prof' : prof}
            return render(request, self.template_name, context)
        except Exception as e:
            logger.error("["+email+"] "+str(e))
        return HttpResponse("Error")

class showCourse(View):

    template_name = 'coursepage.html'

    def get(self,request):
        print "ShowCourse get"
        email = request.session.get('email',None)
        course_id = request.GET.get('courseID',None)
        year = request.GET.get('year',None)
        try:
            logger.info("["+email+"] Retrieving Course Info")
            course = Course.objects.get(courseID=course_id, year=year)
            studentList = CourseGroup.objects.filter(person_group_id=(str.lower(str(course_id))+"_"+str(year)))
            prof = Users.objects.get(ID=course.profID)
            logger.info("["+email+"] Retrieved Course Info Successfully!")
            context = {'course': course, 'prof' : prof, 'studentList' : studentList}
            return render(request, self.template_name, context)
        except Exception as e:
            logger.error("["+email+"] "+str(e))
        return HttpResponse("Error")


class ViewAllQueries(View):
    
    template_name = "viewallqueries.html"

    @method_decorator(assess_role_prof)
    def dispatch(self, request):
        return super(ViewAllQueries, self).dispatch(request)

    def get(self,request):
        print "viewallqueries get"
        email = request.session.get('email',None)
        try:
            logger.info("["+email+"] Retrieving User object")
            prof = Users.objects.get(email=email,role="T")
            logger.info("["+email+"] Retrieved User object Successfully!")
            profID = prof.ID
            logger.debug("profID: "+str(profID))
            courses = Course.objects.filter(profID=profID)
            courseIDs = []
            for course in courses:
                courseIDs.append(course.courseID)
            logger.debug("CourseIDs: "+str(courseIDs))
            allqueries=[]
            logger.info("["+email+"] Retrieving All Queries")
            for courseID in courseIDs:
                queries = Queries.objects.filter(courseID=courseID,resolved=False)
                logger.debug("Query : "+str(queries))
                allqueries.extend(queries)
            logger.info("["+email+"] Retrieved All Queries Successfully!")
            return render(request,self.template_name,{'profID' : profID ,'query_list' : allqueries ,'prof':prof})
        except Exception as e:
            logger.error("["+email+"] "+str(e))
        return HttpResponse("Error")


class ResolveQuery(View):

    def get(self,request,query):
        print "resolvequery get"
        email = request.session.get('email',None)
        queryID = int(query)
        logger.debug("["+email+"] QueryID: "+str(queryID))
        try:
            logger.info("["+email+"] Resolving Query "+str(queryID) )
            queryob = Queries.objects.get(id=queryID)
            queryob.resolved = True
            queryob.save()
            logger.info("["+email+"] Query "+str(queryID)+" Resolved")
            #alert(text='Query Resolved Successfully!', title='Status', button='OK')
            return redirect("/prof/viewallqueries/")
        except Exception as e:
            logger.error("["+email+"] "+str(e))
        return HttpResponse("Error")

class UpdateAttendace(View):

    template_name = 'add.html'

    @method_decorator(assess_role_prof)
    def dispatch(self, request):
        return super(UpdateAttendace, self).dispatch(request)

    def get(self, request):
        print 'UpdateAttendance get'
        email = request.session['email']  
        prof = Users.objects.get(email=email,role="T")
        logger.info("["+email+"] Updating Attendance")
        form = UpdateAttendanceForm()
        return render(request,self.template_name,{'header' : "Update Attendance",'form' : form,'prof':prof })

    def post(self, request, **kwargs):
        print 'UpdateAttendance post'
        form = UpdateAttendanceForm(request.POST)
        email = request.session.get('email',None)
        if form.is_valid():
            print 'valid form'
            logger.info("["+email+"] UpdateAttendance Valid Form")
            date = form.cleaned_data['date']
            courseID = form.cleaned_data['courseID']
            studentID = form.cleaned_data['studentID']
            attendance = form.cleaned_data['attendance']
            year = date.year
            logger.debug("year: "+str(year))
            try:
                logger.info("["+email+"] Retrieveing Attendance Object")
                att = Attendance.objects.get(date=date,courseID=courseID,studentID=studentID,year=year)
                logger.info("["+email+"] Marking Attendance")
                if attendance == "P":
                    att.present = True
                else:
                    att.present = False
                att.save()
                logger.info("["+email+"] Updated Attendance Object")
                #alert(text='Attendance Updated Successfully!', title='Status', button='OK')
                return redirect("/prof/profhome/")
            except Exception as e:
                logger.error("["+email+"] "+str(e))
                return HttpResponse("Error")
        else:
            logger.error("["+email+"] Invalid Form")
            return HttpResponse("Error")
