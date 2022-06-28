from django.db import IntegrityError
from rest_framework.decorators import api_view

from .serializers import UserSerializer
from .models import User
from rest_framework.response import Response
from rest_framework import status

# Create your views here.

@api_view(http_method_names=['Post'])
def register_user(request):
    try:
        user = User.objects.get(email=request.data["email"])
        return Response({"data":"User Already exists!"},status=status.HTTP_400_BAD_REQUEST)
    except User.DoesNotExist:
        user = User.objects.create_user(**request.data)
        serializer = UserSerializer(user)
        return Response({"data":serializer.data})

