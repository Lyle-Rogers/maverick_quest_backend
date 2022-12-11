from rest_framework import serializers
from django.contrib.auth.models import User

from .models import *

class RegisterSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ['id', 'username', 'password']
    write_only_fields = ['password']

  def create(self, validated_data):
    password = validated_data.pop('password', None)
    instance = self.Meta.model(**validated_data)
    if password is not None:
      instance.set_password(password)
    instance.save()
    return instance

class UserPropertiesSerializer(serializers.ModelSerializer):
  user = RegisterSerializer()

  class Meta:
    model = UserProperties
    fields = '__all__'  

class JobScopeSerializer(serializers.ModelSerializer):
  class Meta:
    model = JobScope
    fields = '__all__'

class UserJobScopeSerializer(serializers.ModelSerializer):
  user = RegisterSerializer()
  job_scope = JobScopeSerializer()

  class Meta:
    model = UserJobScope
    fields = '__all__'

class StepSerializer(serializers.ModelSerializer):
  job_scope = JobScopeSerializer()
  
  class Meta:
    model = Step
    fields = '__all__'