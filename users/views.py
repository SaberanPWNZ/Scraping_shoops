from rest_framework import generics
from rest_framework.permissions import AllowAny
from users.models import User
from .serializers import UserCreateSerializer


class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [AllowAny]


from django.shortcuts import render

# Create your views here.
