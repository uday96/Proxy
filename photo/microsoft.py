import requests
from .models import CourseGroup,PersonPhoto
from login.models import Users
import json
from ForGreaterGood.settings import MICROSOFT_KEY
import copy
from attendance.models import Attendance

def create_person_group(prof_id,course_id,year):
	group_id = str.lower(str(course_id)) + "_" + str(year)
	url = "https://westus.api.cognitive.microsoft.com/face/v1.0/persongroups/" +group_id
	headers = {
			"Content-Type":'application/json',
			"Ocp-Apim-Subscription-Key": MICROSOFT_KEY
	}

	data = {
		"name":str(course_id),
		"userData":"This is the group for the course"
	}

	response = requests.put(url,headers=headers,data = json.dumps(data))
	if response.status_code == 200:
		print "Successfully created"
	else :
		print "Error in creating group"
		print response.json()

def create_person(course_id,year,student_ids):
	group_id = str.lower(str(course_id)) + "_" + str(year)	
	print group_id
	url = "https://westus.api.cognitive.microsoft.com/face/v1.0/persongroups/" + group_id +"/persons"

	headers = {
			"Content-Type":'application/json',
			"Ocp-Apim-Subscription-Key": MICROSOFT_KEY
	}

	for student_id in student_ids:

		try:
			student = Users.objects.get(ID = student_id,role = 'S')
			name = student.name

			data = {
			   "name" : str(name)
			}
			response = requests.post(url,headers=headers,data = json.dumps(data))

			resp  = response.json()


			if response.status_code == 200:
				person_id = resp['personId']
				person = CourseGroup(person_group_id = group_id,student_id=student_id,person_id = person_id,course_id=course_id,year=year)
				person.save()
				print "person created"
			else:
				print "error in creating person"
				print resp
		except Exception as e:
			print str(e)

def add_person_image(student_id,img_url):
	print img_url
	persons = CourseGroup.objects.filter(student_id = student_id)
	

	headers = {
			"Content-Type":'application/json',
			"Ocp-Apim-Subscription-Key": MICROSOFT_KEY
		}		

	for p in persons:

		url = "https://westus.api.cognitive.microsoft.com/face/v1.0/persongroups/"+p.person_group_id+"/persons/"+p.person_id+"/persistedFaces"
		data = {"url":str(img_url)}
		resp = requests.post(url,headers = headers,data = json.dumps(data))

		if resp.status_code == 200:
			print "face added for " + p.person_group_id
			body = resp.json()
			per_id = body['persistedFaceId']
			ins = PersonPhoto(person_id = p.person_id,persisted_id = per_id,url = img_url)
			ins.save() 
			print "saved in db for " + per_id
		else:
			print "face not added for " + p.person_group_id
			print resp.json()

def detect_faces(course_id,year,date,img_urls):
	group_id = str.lower(str(course_id)) + "_" + str(year)
	headers = {
			"Content-Type":'application/json',
			"Ocp-Apim-Subscription-Key": MICROSOFT_KEY
		}

	url1 = "https://westus.api.cognitive.microsoft.com/face/v1.0/detect"
	url2 = "https://westus.api.cognitive.microsoft.com/face/v1.0/identify"
	mappings = {}
	all_imgs = {}
	for img_url in img_urls:

		data1 = {"url":str(img_url)}
		resp1 = requests.post(url1,headers = headers,data = json.dumps(data1))
		if resp1.status_code == 200:
			print "faces detected for " + img_url
			body = resp1.json()
			n = 0
			while n < len(body) :
				ids = []
				imgs = copy.copy(body[n:n+10])
				for img in imgs:
					all_imgs[img['faceId']] = img['faceRectangle']
					ids.append(img['faceId'])

				data2 = {
						"personGroupId" : str(group_id),
						"faceIds" :ids						
				}

				resp2 = requests.post(url2,headers = headers,data = json.dumps(data2))

				if resp2.status_code == 200:
					print "mappings obtained"
					a = resp2.json()
					for each in a:
						mappings[each['faceId']] = each['candidates'][0]['personId']
				else:
					print "mappings not obtained"

				n = n + 10

		else:
			print "faces not detected for " + img_url

	people = mappings.values()
	faces = mappings.keys()
	
	students = CourseGroup.objects.all(person_group_id = group_id)
	for each in students:
		person_id = each.person_id
		if person_id in people:			
			for m in faces:
				if mappings[m] == person_id:
					rect = all_imgs[m]
					break

			instance = 	Attendance(courseID=course_id,date=date,studentID=each.student_id,present=True,year=year,url=url,top=rect['top'],left=rect['left'],width=rect['width'],height=rect['height'])
			instance.save()
		else:
			instance = Attendance(courseID=course_id,date=date,studentID=each.student_id,present=False,year=year)
			instance.save()




					















		









