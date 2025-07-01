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

from .models import Run, AthleteInfo, Challenge
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


class UserAnnotatedQuerySet:
    queryset = User.objects.annotate(runs_finished=Count("run", filter=Q(run__status=Run.Status.FINISHED)))


class UserViewSet(UserAnnotatedQuerySet, ReadOnlyModelViewSet):
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
        user = UserAnnotatedQuerySet.queryset.get(run=run)
        if user.runs_finished == 10:
            Challenge.objects.create(full_name="Сделай 10 Забегов!",
                                     athlete=user)

        return Response(model_to_dict(run), status=status.HTTP_200_OK)


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


@api_view(["GET"])
def get_challenge_info(request):
    user_id = request.query_params.get("athlete", None)
    if user_id:
        user_queryset = User.objects.filter(pk=user_id)
        if user_queryset:
            user = user_queryset[0]
            challenges = Challenge.objects.filter(athlete=user)

            return Response({"challenges": challenges}, status=status.HTTP_200_OK)

    return Response(
        {"challenges": Challenge.objects.all().values()}, status=status.HTTP_200_OK
    )
