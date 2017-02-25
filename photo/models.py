from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Photos(models.Model):
	name = models.CharField(max_length=64)
	pic = models.ImageField(upload_to='./images/')

	def __str__(self):
		return self.name


class StudentPhoto(models.Model):
	user_name = models.CharField(max_length=50)
	url = models.CharField(max_length=256)

	def __str__(self):
		return self.user_name

class ClassPhoto(models.Model):
	course = models.CharField(max_length=50)
	date = models.DateField()
	url = models.CharField(max_length=256)

	def __str__(self):
		return self.course

class CourseGroup(models.Model):
	person_group_id = models.CharField(max_length=128)
	student_id = models.CharField(max_length=50)
	person_id = models.CharField(max_length=128)
	course_id = models.CharField(max_length=50,default="")
	year = models.IntegerField(default=2017)

	def __str__(self):
		return self.person_id

class PersonPhoto(models.Model):
	person_id = models.CharField(max_length=128)
	persisted_id  = models.CharField(max_length=128)

	def __str__(self):
		return self.persisted_id

