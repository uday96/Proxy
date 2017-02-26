from django.shortcuts import render, redirect
from django.views.generic import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, DeleteView
from django.http import HttpResponse
from .models import Attendance
# from login.models import Users

# Create your views here.

def history(request, info):
    # return HttpResponse("Hello, world. You're at the prof index page.")
    # prof = Users.objects.get(email=email_id)
    [courseID, studentID, year] = info.split(',')
    try:
        attendanceList = Attendance.objects.filter(courseID=courseID, studentID=studentID, year=year)
        context = {'attendance_list': attendanceList, 'courseID' : courseID, 'studentID' : studentID, 'year' : year}
        return render(request, 'attendance/history.html', context)
    except:
        print "Error"
    # context = {'course_list': courseList, 'prof' : prof}
    # return render(request, 'prof/homepage.html', context)
    return HttpResponse("Error")

def showImage(request, attID):
    try:
        attendance = Attendance.objects.get(id=attID)
        context = {'attendance' : attendance}
        return render(request, 'attendance/showImage.html', context)
    except:
        print "Error"
    return HttpResponse("Error")