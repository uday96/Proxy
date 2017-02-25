from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

from .models import Professor, Course

def index(request):
    # return HttpResponse("Hello, world. You're at the prof index page.")
    prof = Professor.objects.order_by('name')[0]
    courseList = Course.objects.filter(profID=prof.profID)
    context = {'course_list': courseList, 'prof' : prof}
    return render(request, 'prof/homepage.html', context)

def showCourse(request, course_id):
    # return HttpResponse("Hello, world. You're at the prof index page.")
    course = Course.objects.get(courseID=course_id)
    # courseList = Course.objects.filter(profID=prof.profID)
    prof = Professor.objects.get(profID=course.profID)
    context = {'course': course, 'prof' : prof}
    return render(request, 'prof/coursepage.html', context)
