import datetime
import urllib
import random
from django.contrib import auth
from django.contrib.auth.signals import user_logged_in
from django.core.exceptions import ImproperlyConfigured
from django.db import models
from django.db.models.manager import EmptyManager
from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import smart_str
from hashlib import sha1 as sha_constructor
from django.utils.translation import ugettext_lazy as _
from django.utils.crypto import constant_time_compare


def get_hexdigest(algorithm, salt, raw_password):
    """
    Returns a string of the hexdigest of the given plaintext password and salt
    using the given algorithm ('md5', 'sha1' or 'crypt').
    """
    raw_password, salt = smart_str(raw_password), smart_str(salt)
    if algorithm == 'sha1':
        return sha_constructor(salt + raw_password).hexdigest()
    raise ValueError("Got unknown password algorithm type in password.")

def check_password(raw_password, enc_password):
    """
    Returns a boolean of whether the raw_password was correct. Handles
    encryption formats behind the scenes.
    """
    algo, salt, hsh = enc_password.split('$')
    return constant_time_compare(hsh, get_hexdigest(algo, salt, raw_password))

def set_password(raw_password):
    	algo = 'sha1'
    	salt = get_hexdigest(algo, str(random.random()), str(random.random()))[:5]
    	hsh = get_hexdigest(algo, salt, raw_password)
    	enc_password = '%s$%s$%s' % (algo, salt, hsh)
    	return enc_password