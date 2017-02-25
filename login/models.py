from __future__ import unicode_literals
from django.db import models
from .functions import set_password
import random

# Create your models here.
class Users(models.Model):
    ID = models.CharField(max_length=100)
    deptID = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    ROLES = (
        ('S', 'Student'),
        ('T', 'Teacher'),
    )
    role = models.CharField(max_length=1, choices=ROLES)
    password = models.CharField(('password'), max_length=128)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
    	#print "raw : "+self.password
    	pwd = self.password
    	if "sha1$" not in pwd:
    		self.password = set_password(pwd)
    	#print "enc : "+self.password
    	super(Users, self).save(*args, **kwargs)