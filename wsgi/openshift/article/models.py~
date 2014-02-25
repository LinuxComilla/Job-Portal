from django.db import models
from time import time
from datetime import date
# Create your models here.

def get_upload_file_name(instance, filename):
    return "uploaded_files/%s_%s" % (str(time()).replace('.','_'), filename)

class Resume(models.Model):
    email = models.EmailField()
    resume = models.FileField(upload_to=get_upload_file_name)
    
    def __unicode__(self):
	return self.email

class Candidate(models.Model):
    email = models.EmailField()
    name = models.TextField()
    location = models.TextField()
    agree = models.CharField(max_length=5)
    gender = models.CharField(max_length = 6)
    exp = models.IntegerField(default=0)
    title = models.TextField()
    company = models.TextField()
    skills = models.TextField()
    sector = models.TextField()
    functional = models.TextField()
    minsalary = models.FloatField(default=0.0)
    qualification = models.TextField()
    specialization = models.TextField()
    certification = models.TextField()
    institute = models.TextField()
    passing = models.IntegerField(default=1940)
    jtype = models.TextField()
    pubdate = models.DateField(default=date.today())
    
    def __unicode__(self):
	return self.email

class Article(models.Model):
    email = models.EmailField()
    confirm_email = models.EmailField()
    passwd = models.TextField()
    confirm_passwd = models.TextField()
    country_code = models.IntegerField()
    mobile_no = models.IntegerField()
    agree = models.TextField()
    
    def __unicode__(self):
	return self.email

class Arctic(models.Model):
    company = models.TextField()
    contact = models.TextField()
    email = models.EmailField()
    website = models.TextField()
    location = models.TextField()
    passwd = models.TextField()
    confirm_passwd = models.TextField()
    country_code = models.IntegerField()
    mobile_no = models.IntegerField()
    agree = models.TextField()
    
    def __unicode__(self):
	return self.email

class Postjob(models.Model):
    email = models.EmailField()
    title = models.TextField()
    description = models.TextField()
    industry = models.TextField()
    functional = models.TextField()
    minexp = models.IntegerField()
    maxexp = models.IntegerField()
    minsalary = models.TextField()
    maxsalary = models.TextField()
    location = models.TextField()
    jtype = models.CharField(max_length=20)
    qualification = models.TextField()
    
    def __unicode__(self):
	return self.email


