from django.contrib.auth.models import User, Group
from rest_framework import serializers


# Serializer和form很像, ModelSerializer和ModelForm很像
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


