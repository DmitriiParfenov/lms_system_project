from rest_framework import generics
from django.shortcuts import render

from users.models import User
from users.serializers import UserSerializer


# Create your views here.
class UserCreateAPIview(generics.CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserListAPIview(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserRetrieveAPIview(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserUpdateAPIview(generics.UpdateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserDeleteAPIview(generics.DestroyAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
