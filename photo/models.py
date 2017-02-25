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


