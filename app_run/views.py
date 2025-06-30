from django.db.models import Count, Q
from django.forms.models import model_to_dict
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404, GenericAPIView, RetrieveAPIView
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from app_run.models import Run, AthleteInfo
from .serializers import RunSerializer, UserSerializer, AthleteInfoSerializer
from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter


@api_view(["GET"])
def company_info(request):
    return Response(
        {
            "company_name": settings.COMPANY_NAME,
            "slogan": settings.SLOGAN,
            "contacts": settings.CONTACTS,
        }
    )


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


class UserPagination(PageNumberPagination):
    page_size_query_param = "size"
    max_page_size = 10


class UserViewSet(ReadOnlyModelViewSet):
    queryset = User.objects.annotate(runs_finished=Count("run", filter=Q(run__status=Run.Status.FINISHED)))
    serializer_class = UserSerializer
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ("first_name", "last_name")
    ordering_fields = ["date_joined"]
    pagination_class = UserPagination

    def get_queryset(self):
        qs = self.queryset
        user_type = self.request.query_params.get("type", None)
        if user_type:
            if user_type == "athlete":
                qs = qs.filter(is_staff=False)
            elif user_type == "coach":
                qs = qs.filter(is_staff=True).exclude(is_superuser=True)

        return qs.exclude(is_superuser=True)


class StartView(APIView):
    def post(self, request, run_id):
        run = get_object_or_404(Run, id=run_id)
        print(run.status)
        if run.status in (Run.Status.FINISHED, Run.Status.IN_PROGRESS):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        run.status = Run.Status.IN_PROGRESS
        run.save()

        return Response(model_to_dict(run), status=status.HTTP_200_OK)


class StopView(APIView):
    def post(self, request, run_id):
        run = get_object_or_404(Run, id=run_id)
        if run.status != Run.Status.IN_PROGRESS:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        run.status = Run.Status.FINISHED
        run.save()

        return Response(model_to_dict(run), status=status.HTTP_200_OK)


class AthleteInfoView(GenericAPIView, RetrieveModelMixin, UpdateModelMixin):
    queryset = UserViewSet.queryset
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
