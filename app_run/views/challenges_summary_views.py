from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.views import APIView

from app_run.serializers import ChallengeListSerializer


class ChallengesSummaryView(APIView):

    def get(self, request, *args, **kwargs):
        queryset = User.objects.all().prefetch_related("challenges")

        response = list()
        for user in queryset:
            for challenge in user.challenges.all():
                if challenge in response:
                    if user not in response[response.index(challenge)]:
                        response[response.index(challenge)].append(user)
                else:
                    response.append(challenge)
                    response[-1] = [user]

        serializer = ChallengeListSerializer(response, many=True)
        return Response(serializer.data)
