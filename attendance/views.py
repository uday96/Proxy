from django.shortcuts import render, redirect
from django.views.generic import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, DeleteView
from django.http import HttpResponse
from .models import Attendance
from login.models import Users
import logging
from django.views.decorators.csrf import csrf_exempt
import datetime

# Get logger
logger = logging.getLogger('backup')

def proccessAttendance(attendanceList):
    logger.info("Proccess Attendance")
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
    logger.info("Proccess Course Attendance")
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
    email = request.session["email"]
    logger.info("["+email+"] Attendance History")
    [courseID, studentID, year] = info.split(',')
    try:
        user = Users.objects.get(email=email)
        role = user.role
        attendanceList = Attendance.objects.filter(courseID=courseID, studentID=studentID, year=year).order_by('-date')
        if role=="S":
            context = {'attendance_list': attendanceList, 'courseID' : courseID, 'studentID' : studentID, 'year' : year,'student':user}
            return render(request, 'attendance/history_student.html', context)
        elif role=="T":
            context = {'attendance_list': attendanceList, 'courseID' : courseID, 'studentID' : studentID, 'year' : year,'prof':user}
            return render(request, 'attendance/history_prof.html', context)
        else:
            logger.error("["+email+"] No Access Rights!")
            return HttpResponse("No Access Rights!")        
    except Exception as e:
        logger.error("Failed to Retrieve Attendance History")
        logger.error(str(e))
    return HttpResponse("Error")

def showImage(request, attID):
    logger.info("Showing Image")
    try:
        attendance = Attendance.objects.get(id=attID)
        context = {'attendance' : attendance}
        return render(request, 'attendance/showImage.html', context)
    except Exception as e:
        logger.error(str(e))
    return HttpResponse("Error")

class IndividualSummary(View):

    def get(self,request):
        email = request.session["email"]
        logger.info("["+email+"] Getting Individual Summary")
        try:
            courseID = request.GET.get("courseID",None)
            studentID = request.GET.get("studentID",None)
            year = int(request.GET.get("year",None))
            logger.debug(str(courseID)+" "+str(studentID)+" "+str(year))
            attendanceList = Attendance.objects.filter(courseID=courseID,studentID=studentID,year=year).order_by('-date')
            summary = proccessAttendance(attendanceList)
            user = Users.objects.get(email=email)
            role = user.role
            if role=="S":
                context = {'summary': summary, 'courseID' : courseID, 'studentID' : studentID, 'year' : year,'student':user}
                return render(request,'attendance/individualSummary_student.html', context)    
            elif role=="T":
                context = {'summary': summary, 'courseID' : courseID, 'studentID' : studentID, 'year' : year,'prof':user}
                return render(request,'attendance/individualSummary_prof.html', context)    
            else:
                logger.error("["+email+"] No Access Rights!")
                return HttpResponse("No Access Rights!")
        except Exception as e:
            logger.error(str(e))
        return HttpResponse("Error")
        
class CourseSummary(View):
    
    template_name = 'attendance/courseSummary.html'

    def get(self,request):
        email = request.session["email"]
        logger.info("["+email+"] Getting Course Summary")
        try:
            courseID = request.GET.get("courseID",None)
            year = int(request.GET.get("year",None))
            logger.debug(str(courseID)+" "+str(year))
            attendanceList = Attendance.objects.filter(courseID=courseID,year=year).order_by('-date')
            summary = proccessCourseAtt(attendanceList)
            prof = Users.objects.get(email=email,role="T")
            logger.debug("Role: "+str(prof.role))
            context = {'summary': summary, 'courseID' : courseID,'year' : year,'prof':prof}
            return render(request, self.template_name, context)
        except Exception as e:
            logger.error(str(e))
        return HttpResponse("Error")

class DateWiseSummary(View):

    template_name = "attendance/datewiseSummary.html"

    @csrf_exempt
    def post(self,request):
        email = request.session["email"]
        logger.info("["+email+"] Getting DateWise Attendance Summary")
        try:
            date_str = request.POST.get("date","")
            courseID = request.POST.get("courseID","")
            year = int(request.POST.get("year",""))
            date = datetime.datetime.strptime(date_str,'%Y-%m-%d')
            logger.debug("date: "+date_str+", course: "+courseID+", year: "+str(year))
            attendanceList = Attendance.objects.filter(courseID=courseID,year=year,date=date)
            summary = proccessAttendance(attendanceList)
            prof = Users.objects.get(email=email,role="T")
            logger.debug("Role: "+str(prof.role))
            context = {'summary' : summary, 'courseID' : courseID, 'year' : year, 'coursedate' : date,'prof':prof}
            return render(request,self.template_name,context)
        except Exception as e:
            logger.error(str(e))
        return HttpResponse("Error")
