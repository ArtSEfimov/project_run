from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from app_run.serializers import ChallengeListSerializer


class ChallengesSummaryView(APIView):

    def get(self, request, *args, **kwargs):
        queryset = User.objects.all().prefetch_related("challenges")

        challenges = dict()
        for user in queryset:
            for challenge in user.challenges.all():
                challenge_full_name = challenge.full_name
                if challenge_full_name in challenges:
                    if user not in challenges[challenge_full_name]:
                        challenges[challenge_full_name].append(user)
                else:
                    challenges[challenge_full_name] = [user]

        to_repr = list()
        for k, v in challenges.items():
            obj = dict()
            obj["full_name"] = k
            obj["athletes"] = v.copy()
            to_repr.append(obj)

        serializer = ChallengeListSerializer(to_repr, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


note = [
    {
        "full_name": "Challenge_name",
        "athletes": [
            {"id": 1,
             "full_name": "FULLNAME",
             "username": "USERNAME",
             },
        ],
    },
]
