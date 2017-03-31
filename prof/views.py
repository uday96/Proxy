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

# Create your views here.

#Decorator Functions
def assess_role_prof(view_func):
    def _decorator(request):
        if ('email' not in request.session) or ('role' not in request.session):
            return redirect("/login/logout/")
        elif request.session.get('role',"")!='T':
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
        form = CourseAddForm()
        return render(request,self.template_name,{'header' : "Add Course",'form' : form })

    def post(self, request, **kwargs):
        print 'AddCourse post'
        form = CourseAddForm(request.POST)
        if form.is_valid():
            print 'valid form'
            name = form.cleaned_data['name']
            courseID = form.cleaned_data['courseID']
            year = form.cleaned_data['year']
            room = form.cleaned_data['room']
            profEmail = request.session['email']
            prof = Users.objects.get(email=profEmail)
            create_person_group(profEmail,courseID,year)
            instance = Course(courseID=courseID, year=year, deptID=prof.deptID, name=name, room=room, profID=prof.ID)
            instance.save()
            #alert(text='Course Created Successfully!', title='Status', button='OK')
            try:
                courseList = Course.objects.filter(profID=prof.ID)
                context = {'course_list': courseList, 'prof' : prof}
                return render(request, 'homepage.html', context)
            except:
                print "Error"
            return HttpResponse("Error")
            # Call the function to create PersonGroup Microsoft API
            # return HttpResponse("courseID, year, profID: " + str(courseID) + "," + str(year) + "," + str(prof.ID))
        else:
            return HttpResponse("Error")

class AddStudents(View):

    template_name = 'add.html'

    def get(self, request, course_info):
        print 'AddStudents get'
        form = StudentAddForm()
        return render(request,self.template_name,{'header' : "Add Student",'form' : form })

    def post(self, request, course_info, **kwargs):
        print 'AddStudents post'
        form = StudentAddForm(request.POST)
        if form.is_valid():
            print 'valid form'
            profEmail = request.session['email']
            prof = Users.objects.get(email=profEmail)
            studentIDs = str(form.cleaned_data['studentIDs']).split(',')
            [course_id, year] = str(course_info).split(',')
            create_person(course_id,year,studentIDs)
            # alert('Success')
            # alert(text='', title='', button='OK')
            # print request.POST
            # Call the function to create PersonGroup Microsoft API
            course = Course.objects.get(courseID=course_id, year=year)
            studentList = CourseGroup.objects.filter(person_group_id=(str.lower(str(course_id))+"_"+str(year)))
            try:
                context = {'course': course, 'prof' : prof, 'studentList' : studentList}
                return render(request, 'coursepage.html', context)
            except:
                print "Error"
            return HttpResponse("Error")
            # return HttpResponse("courseID, studentIDs, profID: " + str(course_id) + "," + str(studentIDs) + "," + str(prof.ID))
        else:
            return HttpResponse("Error")
            

class ProfHome(View):

    template_name = 'homepage.html'

    @method_decorator(assess_role_prof)
    def dispatch(self, request):
        return super(ProfHome, self).dispatch(request)

    def get(self,request):
        print "profhome get"
        email_get = request.GET.get('mail',None)
        email = request.session.get('email',email_get)
        if not email:
                print "Error"
                return HttpResponse("Error")
        try:
            prof = Users.objects.get(email=email,role='T')
            courseList = Course.objects.filter(profID=prof.ID)
            context = {'course_list': courseList, 'prof' : prof}
            return render(request, self.template_name, context)
        except:
            print "Error"
        return HttpResponse("Error")

class showCourse(View):

    template_name = 'coursepage.html'

    def get(self,request):
        course_id = request.GET.get('courseID',None)
        year = request.GET.get('year',None)
        try:
            course = Course.objects.get(courseID=course_id, year=year)
            studentList = CourseGroup.objects.filter(person_group_id=(str.lower(str(course_id))+"_"+str(year)))
            prof = Users.objects.get(ID=course.profID)
            context = {'course': course, 'prof' : prof, 'studentList' : studentList}
            return render(request, self.template_name, context)
        except:
            print "Error"
        return HttpResponse("Error")


class ViewAllQueries(View):
    
    template_name = "viewallqueries.html"

    @method_decorator(assess_role_prof)
    def dispatch(self, request):
        return super(ViewAllQueries, self).dispatch(request)

    def get(self,request):
        print "viewallqueries get"
        email = request.session.get('email',None)
        if not email:
            print "Error"
            return HttpResponse("Error")
        print email
        try:
            prof = Users.objects.get(email=email,role="T")
            profID = prof.ID
            print profID
            courses = Course.objects.filter(profID=profID)
            courseIDs = []
            for course in courses:
                courseIDs.append(course.courseID)
            print courseIDs
            allqueries=[]
            for courseID in courseIDs:
                queries = Queries.objects.filter(courseID=courseID,resolved=False)
                print "q : "+str(queries)
                allqueries.extend(queries)
            print str(allqueries)
            return render(request,self.template_name,{'profID' : profID ,'query_list' : allqueries })
        except:
            print "Error"
        return HttpResponse("Error")


class ResolveQuery(View):

    def get(self,request,query):
        print "resolvequery get"
        queryID = int(query)
        print queryID
        try:
            queryob = Queries.objects.get(id=queryID)
            queryob.resolved = True
            queryob.save()
            print query+" resolved"
            #alert(text='Query Resolved Successfully!', title='Status', button='OK')
            return redirect("/prof/viewallqueries/")
        except:
            print "error"
        return HttpResponse("Error")

class UpdateAttendace(View):

    template_name = 'add.html'

    @method_decorator(assess_role_prof)
    def dispatch(self, request):
        return super(UpdateAttendace, self).dispatch(request)

    def get(self, request):
        print 'UpdateAttendance get'
        form = UpdateAttendanceForm()
        return render(request,self.template_name,{'header' : "Update Attendance",'form' : form })

    def post(self, request, **kwargs):
        print 'UpdateAttendance post'
        form = UpdateAttendanceForm(request.POST)
        print request.POST
        if form.is_valid():
            print 'valid form'
            date = form.cleaned_data['date']
            courseID = form.cleaned_data['courseID']
            studentID = form.cleaned_data['studentID']
            attendance = form.cleaned_data['attendance']
            year = date.year
            print year 
            try:
                att = Attendance.objects.get(date=date,courseID=courseID,studentID=studentID,year=year)
                if attendance == "P":
                    att.present = True
                else:
                    att.present = False
                att.save()
                print "attendance updated"
                #alert(text='Attendance Updated Successfully!', title='Status', button='OK')
                email = request.session.get('email',None)
                if not email:
                    print "Error"
                    return HttpResponse("Error")
                print email
                return redirect("/prof/profhome?mail="+email)
            except:
                print "Couldnt retrieve Attendance"
                return HttpResponse("Error")
        else:
            return HttpResponse("Error")
