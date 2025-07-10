from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from app_run.serializers import ChallengeListSerializer


class ChallengesSummaryView(APIView):

    def get(self, request, *args, **kwargs):
        queryset = User.objects.all().prefetch_related("challenges")

        response = list()
        for user in queryset:
            for challenge in user.challenges.all():
                challenge_full_name = challenge.full_name
                if challenge.full_name in response:
                    if user not in response[response.index(challenge.full_name)]:
                        response[response.index(challenge.full_name)].append(user)
                else:
                    response.append(challenge.full_name)
                    response[-1] = [user]

        serializer = ChallengeListSerializer(response, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
