from __future__ import unicode_literals

from django.db import models
import random

# Create your models here.
class Users(models.Model):
    name = models.CharField(max_length=64)
    email = models.EmailField(max_length=64)
    ROLES = (
        ('S', 'Student'),
        ('T', 'Teacher'),
    )
    role = models.CharField(max_length=1, choices=ROLES)
    password = models.CharField(('password'), max_length=128)

    def __str__(self):
        return self.name
    
    def set_password(self, raw_password):
	    algo = 'sha1'
	    salt = get_hexdigest(algo, str(random.random()), str(random.random()))[:5]
	    hsh = get_hexdigest(algo, salt, raw_password)
	    self.password = '%s$%s$%s' % (algo, salt, hsh)