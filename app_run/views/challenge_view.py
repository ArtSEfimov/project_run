from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from ..models import Challenge
from ..serializers import ChallengeSerializer


@api_view(["GET"])
def get_challenge_info(request):
    user_id = request.query_params.get("athlete", None)
    if user_id:
        user_queryset = User.objects.filter(pk=user_id)
        if user_queryset:
            user = user_queryset[0]
            challenges = Challenge.objects.filter(athlete=user)

            challenge_serializer = ChallengeSerializer(challenges, many=True)
            return Response(challenge_serializer.data, status=status.HTTP_200_OK)

    challenge_serializer = ChallengeSerializer(Challenge.objects.all(), many=True)
    return Response(challenge_serializer.data, status=status.HTTP_200_OK)
