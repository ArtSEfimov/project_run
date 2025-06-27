from django.forms.models import model_to_dict
from rest_framework import filters, status
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from app_run.models import Run
from .serializers import RunSerializer, UserSerializer
from django.contrib.auth.models import User


@api_view(["GET"])
def company_info(request):
    return Response(
        {
            "company_name": settings.COMPANY_NAME,
            "slogan": settings.SLOGAN,
            "contacts": settings.CONTACTS,
        }
    )


class RunViewSet(ModelViewSet):
    queryset = Run.objects.select_related("athlete").all()
    serializer_class = RunSerializer


class UserViewSet(ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ("first_name", "last_name")

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
