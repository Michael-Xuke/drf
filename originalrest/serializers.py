from django.contrib.auth.models import User
from rest_framework import serializers

from originalrest.models import Goods


class GoodsSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=64)
    price = serializers.FloatField()

    owner = serializers.ReadOnlyField(source='owner.username')

    def create(self, validated_data):
        return Goods.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data['name']
        instance.price = validated_data['price']
        instance.save()
        return instance


class GoodsModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goods
        fields = ['id', 'name', 'price']


class UserSerializer(serializers.ModelSerializer):
    goods  = serializers.PrimaryKeyRelatedField(many=True, queryset=Goods.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'goods')


class GoodsHyperLinkedModelSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Goods
        fields = ['url','id', 'name', 'price', 'owner']


class UserHyperLinkedSerializer(serializers.HyperlinkedModelSerializer):
    goods = serializers.HyperlinkedRelatedField(many=True, view_name='goods-detail', read_only=True)

    class Meta:
        model = User
        fields = ('url','id', 'username', 'goods')
