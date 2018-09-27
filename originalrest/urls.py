from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from .views import goods_view, GoodsList, GoodsDetail, UserList, UserDetail, api_root

urlpatterns = [
    # url(r'goods/(?P<pk>\d+)/$', goods_view, name='goods'),
    url(r'goods/(?P<pk>\d+)/$', GoodsDetail.as_view(), name='goods-detail'),
    url(r'goods/$', GoodsList.as_view(), name='goods-list'),

    url(r'^users/$', UserList.as_view(), name='user-list'),
    url(r'^users/(?P<pk>[0-9]+)/$', UserDetail.as_view(), name='user-detail'),
    url(r'^$', api_root),

]
urlpatterns = format_suffix_patterns(urlpatterns)
