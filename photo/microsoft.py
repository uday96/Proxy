import requests
from .models import CourseGroup,PersonPhoto
from login.models import Users
import json
from ForGreaterGood.settings import MICROSOFT_KEY
import copy

def create_person_group(prof_id,course_name,year):
	group_id = str.lower(course_name) + "_" + str(year)
	url = "https://westus.api.cognitive.microsoft.com/face/v1.0/persongroups/" +group_id
	headers = {
			"Content-Type":'application/json',
			"Ocp-Apim-Subscription-Key": MICROSOFT_KEY
	}

	data = {
		"name":course_name,
		"userData":"This is the group for the course"
	}

	response = requests.post(url,headers=headers,data = data)
	if response.status_code == 200:
		print "Successfully created"
	else :
		print "Error in creating group"

def create_person(course_name,year,student_ids):
	group_id = str.lower(course_name) + "_" + str(year)	
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
			   "name" : name
			}
			response = requests.post(url,headers=headers,data = data)

			resp  = response.json()


			if response.status_code == 200:
				person_id = resp['personId']
				person = CourseGroup(person_group_id = group_id,student_id=student_id,person_id = person_id)
				person.save()
				print "person created"
			else:
				print "error in creating person"
		except Exception as e:
			print str(e)

def add_person_image(student_id,img_url):
	persons = PersonPhoto.objects.all(student_id = student_id)
	

	headers = {
			"Content-Type":'application/json',
			"Ocp-Apim-Subscription-Key": MICROSOFT_KEY
		}		

	for p in persons:

		url = "https://westus.api.cognitive.microsoft.com/face/v1.0/persongroups/"+p.person_group_id+"/persons/"+p.person_id+"/persistedFaces"
		data = {"url":img_url}
		resp = requests.post(url,headers = headers,data = data)

		if resp.status_code == 200:
			print "face added for " + p.person_group_id
			body = resp.json()
			per_id = body['persistedFaceId']
			ins = PersonPhoto(person_id = person_id,persisted_id = per_id,url = img_url)
			ins.save() 
			print "saved in db for " + per_id
		else:
			print "face not added for " + p.person_group_id

def detect_faces(group_id,date,img_urls):

	headers = {
			"Content-Type":'application/json',
			"Ocp-Apim-Subscription-Key": MICROSOFT_KEY
		}

	url1 = "https://westus.api.cognitive.microsoft.com/face/v1.0/detect"
	url2 = "https://westus.api.cognitive.microsoft.com/face/v1.0/identify"
	mappings = {}
	for img_url in img_urls:

		data1 = {"url":img_url}
		resp1 = requests.post(url1,headers = headers,data = data1)
		if resp1.status_code == 200:
			print "faces detected for " + img_url
			body = resp1.json()
			n = 0
			while n < len(body) :
				ids = []
				imgs = copy.copy(body[n:n+10])
				for img in imgs:
					ids.append(img['faceId'])

				data2 = {
						"personGroupId" : group_id,
						"faceIds" :ids						
				}

				resp2 = requests.post(url2,headers = headers,data = data2)

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

					















		









