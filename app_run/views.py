from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from app_run.models import Run
from .serializers import RunSerializer, UserSerializer
from django.contrib.auth.models import User


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
    queryset = Run.objects.select_related('athlete').all()
    serializer_class = RunSerializer

    def perform_create(self, serializer):
        serializer.save(athlete=self.request.user)


class UserViewSet(ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        qs = self.queryset
        user_type = self.request.query_params.get('type', None)
        if user_type:
            if user_type == 'athlete':
                qs = qs.filter(is_staff=False)
            elif user_type == 'coach':
                qs = qs.filter(is_staff=True).exclude(is_superuser=True)

        return qs.exclude(is_superuser=True)
