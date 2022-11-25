from rest_framework.views import APIView
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest_framework.response import Response

from .serializers import *
from .throttling import *
from .permissions import *

@permission_classes([AllowAny])
class LoginView(APIView):
  # throttle_classes = []

  def post(self, request):
    username = request.data['username']
    password = request.data['password']

    try:
      user = User.objects.get(username=username)
    except:
      return Response('Invalid username')

    if not user.check_password(password):
      return Response('Invalid password')

    auth_token = Token.objects.get_or_create(user = user.id)

    return Response(
      {"user_id": user.id, "auth_token": str(auth_token[0])},
      status = status.HTTP_200_OK
    )

@permission_classes([AllowAny])
class RegisterView(APIView):
  # throttle_classes = []

  def post(self, request):
    username = request.data['username']

    username_registered = User.objects.get(username=username)

    if username_registered:
      return Response('Username is already registered')

    registerSerializer = RegisterSerializer(data = request.data)
    registerSerializer.is_valid(raise_exception = True)
    registerSerializer.save()

    user = User.objects.get(id = registerSerializer.data['id'])
    
    userPropertiesSerializer = UserPropertiesSerializer(data = None, partial = True)
    userPropertiesSerializer.is_valid(raise_exception = True)
    userPropertiesSerializer.save(user = user)

    auth_token = Token.objects.create(user = user)

    return Response(
      {'user_id': user.id, 'auth_token': auth_token.key},
      status = status.HTTP_200_OK
    )
