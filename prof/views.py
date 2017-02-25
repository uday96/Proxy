from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

from .models import Course
from login.models import Users

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

def showCourse(request, course_id):
    # return HttpResponse("Hello, world. You're at the prof index page.")
    # print course_id
    course = Course.objects.get(courseID=course_id)
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
