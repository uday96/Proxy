from django.shortcuts import render, redirect
from django.views.generic import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, DeleteView
from django.http import HttpResponse
from .models import Course
from login.models import Users
from .forms import CourseAddForm, StudentAddForm
from photo.microsoft import create_person,create_person_group
# Create your views here.

class AddCourse(View):
    template_name = 'prof/add.html'

    def get(self, request):
        print 'AddCourse get'
        form = CourseAddForm()
        return render(request,self.template_name,{'form' : form })

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
            create_person_group(profEmail,name,year)
            
            alert('Success')
            try:
                courseList = Course.objects.filter(profID=prof.ID)
                context = {'course_list': courseList, 'prof' : prof}
                return render(request, 'prof/homepage.html', context)
            except:
                print "Error"
            return HttpResponse("Error")
            # Call the function to create PersonGroup Microsoft API
            # return HttpResponse("courseID, year, profID: " + str(courseID) + "," + str(year) + "," + str(prof.ID))
        else:
            return HttpResponse("Error")

class AddStudents(View):
    template_name = 'prof/add.html'

    def get(self, request, course_info):
        print 'AddStudents get'
        form = StudentAddForm()
        return render(request,self.template_name,{'form' : form })

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
            alert('Success')
            # print request.POST
            # Call the function to create PersonGroup Microsoft API
            course = Course.objects.get(courseID=course_id, year=year)
            try:
                context = {'course': course, 'prof' : prof}
                return render(request, 'prof/coursepage.html', context)
            except:
                print "Error"
            return HttpResponse("Error")
            # return HttpResponse("courseID, studentIDs, profID: " + str(course_id) + "," + str(studentIDs) + "," + str(prof.ID))
        else:
            return HttpResponse("Error")
            

def homePage(request, email_id):
    # return HttpResponse("Hello, world. You're at the prof index page.")
    prof = Users.objects.get(email=email_id)
    try:
        courseList = Course.objects.filter(profID=prof.ID)
        context = {'course_list': courseList, 'prof' : prof}
        return render(request, 'prof/homepage.html', context)
    except:
        print "Error"
    # context = {'course_list': courseList, 'prof' : prof}
    # return render(request, 'prof/homepage.html', context)
    return HttpResponse("Error")

def showCourse(request, course_info):
    # return HttpResponse("Hello, world. You're at the prof index page.")
    # print course_id
    [course_id, year] = str(course_info).split(',')
    course = Course.objects.get(courseID=course_id, year=year)
    # print course.profID
    # courseList = Course.objects.filter(profID=prof.profID)
    try:
        prof = Users.objects.get(ID=course.profID)
        context = {'course': course, 'prof' : prof}
        # print context
        return render(request, 'prof/coursepage.html', context)
    except:
        print "Error"
    return HttpResponse("Error")
