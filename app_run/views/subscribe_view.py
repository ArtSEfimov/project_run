from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from app_run.models import Subscribe
from app_run.serializers import SubscribeSerializer


class SubscribeCreateView(APIView):

    def post(self, request, *args, **kwargs):
        athlete_id = request.data.get('athlete')
        coach_id = self.kwargs.get('id')

        coach = get_object_or_404(User, id=coach_id)
        if not coach.is_staff:
            return Response({"message": "user is not a coach"}, status=status.HTTP_400_BAD_REQUEST)

        athletes = User.objects.filter(id=athlete_id, is_staff=False)
        if not athletes.exists():
            return Response({"message": "athlete not found"}, status=status.HTTP_400_BAD_REQUEST)

        athlete = athletes.first()
        subscribes = Subscribe.objects.filter(athlete=athlete, coach=coach)
        if subscribes.exists():
            return Response({"message": "subscribe already exists"}, status=status.HTTP_400_BAD_REQUEST)

        subscribe = Subscribe.objects.create(athlete=athlete, coach=coach)
        serializer = SubscribeSerializer(instance=subscribe)
        return Response(serializer.data, status=status.HTTP_200_OK)
