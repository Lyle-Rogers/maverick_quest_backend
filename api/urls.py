from django.urls import path

from .views import *

urlpatterns = [
    path('automatic_login', AutomaticLoginView.as_view()),
    path("login", LoginView.as_view()),
    path("register", RegisterView.as_view()),
    path('upload_job_scope_video', UploadJobScopeVideoView.as_view()),
    path('stream_job_scope_video/<int:pk>', StreamJobScopeVideoView.as_view()),
]
