from django.urls import path
from . import views
from .customAuthToken import CustomAuthToken


urlpatterns = [
    path('register/',view=views.register_user),
    path('login/', view= CustomAuthToken.as_view())
]