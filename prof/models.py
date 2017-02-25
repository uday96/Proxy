from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Course(models.Model):
	name = models.CharField(max_length=100)
	courseID = models.CharField(max_length=100)
	deptID = models.CharField(max_length=100)
	room = models.CharField(max_length=100)
	year = models.IntegerField(default=2017)
	profID = models.CharField(max_length=100)
