from django.contrib.auth.models import User
from django.http import Http404, JsonResponse, HttpResponseBadRequest, QueryDict
from django.shortcuts import render, get_object_or_404

# Create your views here.

# 原生rest
# 实现增删改查.
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status, mixins, generics, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.reverse import reverse

from originalrest.models import Goods
from originalrest.permissions import IsOwnerOrReadOnly
from originalrest.serializers import GoodsSerializer, UserSerializer, GoodsHyperLinkedModelSerializer, \
    UserHyperLinkedSerializer


# @csrf_exempt
@api_view(['GET', 'PUT', 'DELETE', 'POST'])
def goods_view(request, pk):
    # 获取数据
    if request.method == 'GET':
        if int(pk) == 0:
            goods_list = Goods.objects.all()
            serializer = GoodsSerializer(goods_list, many=True)
            data = {
                'status': 200,
                'msg': 'success',
                # 'data': [object.to_dict() for object in goods_list]
                'data': serializer.data
            }

            # return JsonResponse(data)
            return Response(data)
        else:
            goods = get_object_or_404(Goods, pk=pk)
            return JsonResponse(goods.to_dict())
    elif request.method == 'POST':
        name = request.POST.get('name', None)
        price = request.POST.get('price', None)
        if name and price:
            goods = Goods.objects.create(name=name, price=price)
            data = {
                'status': 201,
                'msg': 'create success',
                'data': goods.to_dict()
            }
            # 使用rest_framework 的response来替换JsonResponse,实现客户端要什么,就返回什么格式的效果.
            return JsonResponse(data)
            # return Response(data)
        else:
            raise HttpResponseBadRequest
    elif request.method == 'PUT':
        # 使用request.body获取put请求提交的数据
        # put_data = QueryDict(request.body.decode('utf-8'), encoding='utf-8')
        # name = put_data.get('name', None)
        # price = put_data.get('price', None)
        # name = request.data.get('name')
        # print(name)
        # 改成使用serializer写
        try:
            goods = Goods.objects.get(pk=pk)
        except Goods.DoesNotExist:
            print('是不是 找不到啊')
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = GoodsSerializer(goods, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        pass
    else:
        raise Http404


# class GoodsList(APIView):
#     def get(self, request, format=None):
#         goods_list = Goods.objects.all()
#         serializer = GoodsSerializer(goods_list, many=True)
#         return Response(serializer.data)
#
#     def post(self, request, format=None):
#         serializer = GoodsSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def perform_create(self, serializer):
#         serializer.save(owner= self.request.user)



class GoodsList(generics.ListCreateAPIView):
    queryset = Goods.objects.all()
    serializer_class = GoodsHyperLinkedModelSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(owner= self.request.user)

# class GoodsDetail(mixins.RetrieveModelMixin,
#                   mixins.UpdateModelMixin,
#                   mixins.DestroyModelMixin,
#                   generics.GenericAPIView):
#     queryset = Goods.objects.all()
#     serializer_class = GoodsSerializer
#
#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)
#
#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)
#
#     def delete(self, request, *args, **kwrags):
#         return self.destroy(request, *args, **kwrags)


class GoodsDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Goods.objects.all()
    serializer_class = GoodsHyperLinkedModelSerializer

    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserHyperLinkedSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserHyperLinkedSerializer


@api_view(['GET'])
def api_root(request, format=None):
    return Response(
        {
            'goods': reverse('goods-list', request=request, format=format)
        }
    )
