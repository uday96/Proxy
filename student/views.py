from django.shortcuts import render, redirect
from django.views.generic import View
from login.models import Users
from django.http import HttpResponse

# Create your views here.
class StudentHome(View):
	
	template_name = "studenthome.html"

	def get(self,request):
		email = request.GET.get('mail',None)
		if not email:
			print "Error"
			return HttpResponse("Error")
		
		student = Users.objects.get(email=email,role="S")
		try:
			context = {'student' : student}
			print context
			return render(request,self.template_name,context)
		except:
			print "Error"
		return HttpResponse("Error")