from rest_framework.views import APIView
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest_framework.response import Response

from django.http import HttpResponse
from wsgiref.util import FileWrapper
from django.http import FileResponse
import os

from .serializers import *
from .throttling import *
from .permissions import *

@permission_classes([AllowAny])
class AutomaticLoginView(APIView):
  # throttle_classes = [AutomaticLoginUserThrottle, AutomaticLoginAnonThrottle]
  
  def post(self, request):
    try:
      auth_token = Token.objects.get(key = request.data['auth_token'])
    except:
      return Response('Token is invalid')

    return Response(
      status=status.HTTP_200_OK
    )

@permission_classes([AllowAny])
class LoginView(APIView):
    # throttle_classes = []

    def post(self, request):
        username = request.data["username"]
        password = request.data["password"]

        try:
            user = User.objects.get(username=username)
        except:
            return Response("Invalid username")

        if not user.check_password(password):
            return Response("Invalid password")

        auth_token = Token.objects.get_or_create(user=user)

        return Response(
            {"user_id": user.id, "auth_token": str(auth_token[0])},
            status=status.HTTP_200_OK,
        )


@permission_classes([AllowAny])
class RegisterView(APIView):
    # throttle_classes = []

    def post(self, request):
        username = request.data["username"]

        try:
            username_registered = User.objects.get(username=username)
            return Response("That username is already registered")
        except:
            pass

        registerSerializer = RegisterSerializer(data=request.data)
        registerSerializer.is_valid(raise_exception=True)
        registerSerializer.save()

        user = User.objects.get(id=registerSerializer.data["id"])

        userPropertiesSerializer = UserPropertiesSerializer(data={'admin': False}, partial=True)
        userPropertiesSerializer.is_valid(raise_exception=True)
        userPropertiesSerializer.save(user=user)

        auth_token = Token.objects.create(user=user)

        return Response(
            {"user_id": user.id, "auth_token": auth_token.key},
            status=status.HTTP_200_OK,
        )

class UploadJobScopeVideoView(APIView): 
    def post(self, request):
        if 'video' not in request.FILES:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        jobScopeSerializer = JobScopeSerializer(data=request.data, partial=True)
        jobScopeSerializer.is_valid(raise_exception=True)
        jobScopeSerializer.save()

        return Response(status=status.HTTP_200_OK)

class StreamJobScopeVideoView(APIView):
    def get(self, request, pk):
        video_path = 'media/video/Southpark_-_1302_-_The_Coon_C_P_2niTNUa.mp4'
        file = FileWrapper(open(video_path, 'rb').read())
        response = HttpResponse(file, content_type='video/mp4')
        response['Content-Disposition'] = 'attachment; filename=my_video.mp4'

        return response

        # jobScope = JobScope.objects.get(pk=pk)

        # video = jobScope.video

        # return FileResponse(video, content_type='video/mp4')
        # return FileResponse(open('media/' + str(video), 'rb'), content_type='video/mp4')
        # return FileResponse(open('media/video/Southpark_-_1302_-_The_Coon_C_P_2niTNUa.mp4'), content_type='video/mp4')

        # video_path = 'media/video/Southpark_-_1302_-_The_Coon_C_P_2niTNUa.mp4'
        # video_data = open(video_path, 'rb').read()
        # response = Response(video_data, content_type='video/mp4')
        # return response

        # video_path = 'media/video/Southpark_-_1302_-_The_Coon_C_P_2niTNUa.mp4'
        # if os.path.exists(video_path):
        #     with open(video_path, 'rb') as f:
        #         video_data = f.read()
        #     response = Response(video_data, content_type='video/mp4')
        #     return response
        # else:
        #     return Response(status=status.HTTP_404_NOT_FOUND)
