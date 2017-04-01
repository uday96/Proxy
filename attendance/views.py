from django.shortcuts import render, redirect
from django.views.generic import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, DeleteView
from django.http import HttpResponse
from .models import Attendance
# from login.models import Users

# Create your views here.

def proccessAttendance(attendanceList):
    print "proccess attendance"
    present=[]
    absent=[]
    for attendance in attendanceList:
        if attendance.present ==True:
            present.append(attendance)
        else:
            absent.append(attendance)
    summary = {
            'present':present,
            'absent':absent,
            'count_present':len(present),
            'count_absent':len(absent),
            'total':len(attendanceList)
            }
    return summary

def proccessCourseAtt(attendanceList):
    print "proccess Course Attendance"
    datewise = {}
    for attendance in attendanceList:
        date = attendance.date
        if datewise.has_key(date):
            if attendance.present ==True:
                datewise[date]["present"].append(attendance)
            else:
                datewise[date]["absent"].append(attendance)
        else:
            datewise[date] = {"present":[],"absent":[]}
            if attendance.present ==True:
                datewise[date]["present"].append(attendance)
            else:
                datewise[date]["absent"].append(attendance)
            
    classes_taken = len(datewise)
    summary = {'classes':classes_taken,'datewise':[]}
    for key in datewise.keys():
        summary["datewise"].append({
            "date":key,
            "present":datewise[key]["present"],
            "absent":datewise[key]["absent"],
            'count_present':len(datewise[key]["present"]),
            'count_absent':len(datewise[key]["absent"]),
            })

    return summary


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

class IndividualSummary(View):
    
    template_name = 'attendance/individualSummary.html'

    def get(self,request):
        print "IndividualSummary get"
        try:
            courseID = request.GET.get("courseID",None)
            studentID = request.GET.get("studentID",None)
            year = int(request.GET.get("year",None))
            print courseID, studentID, year
            attendanceList = Attendance.objects.filter(courseID=courseID,studentID=studentID,year=year)
            summary = proccessAttendance(attendanceList)
            context = {'summary': summary, 'courseID' : courseID, 'studentID' : studentID, 'year' : year}
            return render(request, self.template_name, context)
        except Exception as e:
            print str(e)
        return HttpResponse("Error")
        
class CourseSummary(View):
    
    template_name = 'attendance/courseSummary.html'

    def get(self,request):
        print "CourseSummary get"
        try:
            courseID = request.GET.get("courseID",None)
            year = int(request.GET.get("year",None))
            print courseID, year
            attendanceList = Attendance.objects.filter(courseID=courseID,year=year)
            summary = proccessCourseAtt(attendanceList)
            context = {'summary': summary, 'courseID' : courseID,'year' : year}
            return render(request, self.template_name, context)
        except Exception as e:
            print str(e)
        return HttpResponse("Error")