from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import Subscribe
from ..serializers import SubscribeSerializer


class RateCoachView(APIView):

    def post(self, request, *args, **kwargs):
        athlete_id = request.data.get("athlete", None)
        score = request.data.get("rating", None)

        coach_id = self.kwargs.get("coach_id")

        coach = get_object_or_404(User, id=coach_id)

        if athlete_id is None:
            return Response({"message": "athlete_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        athletes = User.objects.filter(id=athlete_id)
        if not athletes.exists():
            return Response({"message": "athlete not found"}, status=status.HTTP_400_BAD_REQUEST)

        athlete = athletes.first()

        if score is None or not isinstance(score, int):
            return Response({"message": "Score must be an integer"},
                            status=status.HTTP_400_BAD_REQUEST)
        if score > 5 or score < 1:
            return Response({"message": "score value must be in the range 1 to 5."},
                            status=status.HTTP_400_BAD_REQUEST)

        subscribes = Subscribe.objects.filter(athlete=athlete, coach=coach)
        if not subscribes.exists():
            return Response({"message": "subscribe does not exist"}, status=status.HTTP_400_BAD_REQUEST)

        subscribe = subscribes.first()
        subscribe.score = score
        subscribe.save()

        serializer = SubscribeSerializer(instance=subscribe)
        return Response(serializer.data, status=status.HTTP_200_OK)
