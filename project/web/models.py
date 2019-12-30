from django.db import models

'''用户'''
class User(models.Model):
    name = models.CharField(max_length=128,unique=True)
    password = models.CharField(max_length=256)
    email = models.EmailField(unique=True)

'''作品'''
class Work(models.Model):
    name = models.TextField()
    date = models.TextField()
    carrier = models.TextField()
    introduction = models.TextField()
