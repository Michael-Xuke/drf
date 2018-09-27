from django.shortcuts import render
from django.contrib.auth.models import  User, Group
from rest_framework import viewsets

# Create your views here.


# ModelViewSet提供对模型的增删改查功能
from quickstart.serializers import UserSerializer, GroupSerializer


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all().order_by('-date_joined')


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
