from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Attendance(models.Model):
    courseID = models.CharField(default='', max_length=100)
    date = models.DateField()
    studentID = models.CharField(default='', max_length=100)
    present = models.BooleanField(default=False)
    year = models.IntegerField(default=2017)