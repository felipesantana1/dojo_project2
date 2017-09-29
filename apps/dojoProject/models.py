from __future__ import unicode_literals
from django.db import models
import re
import bcrypt
from datetime import datetime

PASSWORD_REGEX = re.compile(r'[A-Z0-9]')

class UsersManager(models.Manager):

    def regValidator(self, postData):
        errors = {}
        if len(postData['name']) < 3:
            errors['name'] = 'Name field must contain at least 3 characters'
        if len(postData['username']) < 3:
            errors['username'] = 'Username field must contain at least 3 characters'
        if len(postData['password']) < 8:
            errors['password'] = 'Password must contain more than 8 characters'
        if not PASSWORD_REGEX.match(postData['password']):
            errors['password'] = 'Invalid email/password'
        if postData['password'] != postData['confirmPW']:
            errors['password'] = 'Passwords do not match!'
        if len(postData['date']) == 0:
            errors['date'] = 'Date hired must be entered '
        return errors

    def logValidator(self, postData):
        errors = {}
        if postData['username'] < 1:
            errors['username'] = 'No username/password detected. Please try again.'
        if postData['password'] < 1:
            errors['password'] = 'No username/password detected. Please try again.'
        if not Users.objects.filter(username=postData['username']):
            errors['login'] = 'Invalid username/password. Please try again or register'
        elif not bcrypt.checkpw(postData['password'].encode(), Users.objects.get(username=postData['username']).password.encode()):
            errors['login'] = 'Invalid username/password. Please try again or register'
        return errors


class Users(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    hired = models.DateField(auto_now=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UsersManager()

class Wishes(models.Model):
    name = models.CharField(max_length=255)
    wish = models.ManyToManyField(Users, related_name='wish_for')
    user = models.ForeignKey(Users, related_name='wish')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)