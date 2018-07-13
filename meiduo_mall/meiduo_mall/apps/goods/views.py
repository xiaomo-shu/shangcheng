from django.shortcuts import render
from drf_haystack.viewsets import HaystackViewSet
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView

from .serializers import SKUSerializer, SKUIndexSerializer
from .models import SKU
# Create your views here.


class SKUSearchViewSet(HaystackViewSet):
    # 索引对应模型类
    index_models = [SKU]

    serializer_class = SKUIndexSerializer


# GET /categories/(?P<category_id>\d+)/skus/?page=xxx&page_size=xxx&ordering=xxx
class SKUListView(ListAPIView):
    serializer_class = SKUSerializer

    # 排序
    filter_backends = (OrderingFilter,)
    ordering_fields = ('create_time', 'price', 'sales')

    def get_queryset(self):
        # 获取分类id
        category_id = self.kwargs['category_id']

        return SKU.objects.filter(category_id=category_id, is_launched=True)