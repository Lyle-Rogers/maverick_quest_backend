from django.db import models
from django.contrib.auth.models import User

class UserProperties(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)  
  admin = models.BooleanField(default=False)
  profile_image = models.URLField(max_length=255, blank=True, null=True)

class JobScope(models.Model):
  name = models.CharField(max_length=255, blank=True, null=True)
  video = models.URLField(max_length=255, blank=True, null=True)

class UserJobScope(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  job_scope = models.ForeignKey(JobScope, on_delete=models.CASCADE)
  time_ends = models.DateTimeField()

class Step(models.Model):
  job_scope = models.ForeignKey(JobScope, on_delete=models.CASCADE)
  placement = models.IntegerField()
  description = models.TextField(max_length=255, blank=True, null=True)
  step_video = models.URLField(max_length=255, blank=True, null=True)
  step_image = models.URLField(max_length=255, blank=True, null=True)
