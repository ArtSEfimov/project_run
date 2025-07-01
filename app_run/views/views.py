from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings
from django.contrib.auth.models import User

from ..models import Challenge


@api_view(["GET"])
def company_info(request):
    return Response(
        {
            "company_name": settings.COMPANY_NAME,
            "slogan": settings.SLOGAN,
            "contacts": settings.CONTACTS,
        }
    )


@api_view(["GET"])
def get_challenge_info(request):
    user_id = request.query_params.get("athlete", None)
    if user_id:
        user_queryset = User.objects.filter(pk=user_id)
        if user_queryset:
            user = user_queryset[0]
            challenges = Challenge.objects.filter(athlete=user)

            return Response(challenges, status=status.HTTP_200_OK)

    return Response(
        Challenge.objects.all(), status=status.HTTP_200_OK
    )
