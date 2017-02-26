from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Attendance(models.Model):
    courseID = models.CharField(default='', max_length=100)
    date = models.DateField()
    studentID = models.CharField(default='', max_length=100)
    present = models.BooleanField(default=False)
    year = models.IntegerField(default=2017)
    url = models.CharField(default='', max_length=200)
    top = models.IntegerField(default=0)
    left = models.IntegerField(default=0)
    height = models.IntegerField(default=0)
    width = models.IntegerField(default=0)

    def __str__(self):
        return str(self.date)+"_"+self.courseID+"_"+self.studentID