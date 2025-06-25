from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings
from rest_framework.viewsets import ModelViewSet

from app_run.models import Run
from .serializers import RunSerializer


@api_view(['GET'])
def company_info(request):
    return Response(
        {
            'company_name': settings.COMPANY_NAME,
            'slogan': settings.SLOGAN,
            'contacts': settings.CONTACTS,
        }
    )


class RunViewSet(ModelViewSet):
    queryset = Run.objects.all()
    serializer_class = RunSerializer
