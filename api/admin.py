from django.contrib import admin

from .models import *

@admin.register(UserProperties)
class UserProperties(admin.ModelAdmin):
  list_display = ['user', 'admin']

@admin.register(JobScope)
class JobScope(admin.ModelAdmin):
  list_display = ['name']

@admin.register(UserJobScope)
class UserJobScope(admin.ModelAdmin):
  list_display = ['user', 'job_scope', 'time_ends']

@admin.register(Step)
class Step(admin.ModelAdmin):
  list_display = ['job_scope', 'placement', 'description']


  
