from django.db.models.aggregates import Avg
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ReadOnlyModelViewSet

from .views import UserAnnotatedQuerySet
from ..models import AthleteInfo
from ..serializers import UserListSerializer, AthleteInfoSerializer, UserDetailSerializer


class UserPagination(PageNumberPagination):
    page_size_query_param = "size"
    max_page_size = 10


class UserViewSet(UserAnnotatedQuerySet, ReadOnlyModelViewSet):
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ("first_name", "last_name")
    ordering_fields = ["date_joined"]
    pagination_class = UserPagination
    lookup_url_kwarg = "id"

    def get_serializer_class(self):
        if self.action == "retrieve":
            return UserDetailSerializer
        return UserListSerializer

    def get_queryset(self):
        qs = self.queryset
        user_type = self.request.query_params.get("type", None)
        if user_type:
            if user_type == "athlete":
                qs = qs.filter(is_staff=False)
            elif user_type == "coach":
                qs = qs.filter(is_staff=True)

        return qs.exclude(is_superuser=True).annotate(rating=Avg("coach_subscribes__score"))

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        if self.action == "retrieve":
            ctx["user"] = self.get_object()

        return ctx


class AthleteInfoView(UserAnnotatedQuerySet, GenericAPIView, RetrieveModelMixin, UpdateModelMixin):
    serializer_class = AthleteInfoSerializer
    lookup_url_kwarg = "user_id"

    def get_object(self):
        user_object = super().get_object()
        info_object, is_created = AthleteInfo.objects.get_or_create(user=user_object)
        return info_object

    def put(self, request, user_id):
        return self.update(request, user_id)

    def get(self, request, user_id):
        return self.retrieve(request, user_id)
