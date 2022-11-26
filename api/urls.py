from django.urls import path

from .views import *

urlpatterns = [
    path('automatic_login', AutomaticLoginView.as_view()),
    path("login", LoginView.as_view()),
    path("register", RegisterView.as_view()),
]
