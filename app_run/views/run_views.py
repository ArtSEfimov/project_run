from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import OrderingFilter

from ..models import Run
from ..serializers import RunSerializer


class RunPagination(PageNumberPagination):
    page_size_query_param = "size"
    max_page_size = 10


class RunViewSet(ModelViewSet):
    queryset = Run.objects.select_related("athlete").all()
    serializer_class = RunSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_fields = ("status", "athlete")
    ordering_fields = ["created_at"]
    pagination_class = RunPagination
