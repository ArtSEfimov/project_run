from django.conf import settings
from django.contrib.auth.models import User
from django.db.models import Count, Q
from rest_framework.decorators import api_view
from rest_framework.response import Response

from ..models import Run


class UserAnnotatedQuerySet:
    queryset = User.objects.annotate(runs_finished=Count("run", filter=Q(run__status=Run.Status.FINISHED)))


@api_view(["GET"])
def company_info(request):
    return Response({"company_name": settings.COMPANY_NAME, "slogan": settings.SLOGAN, "contacts": settings.CONTACTS, })
