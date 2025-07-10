from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from app_run.models import Subscribe


class SubscribeCreateView(APIView):

    def post(self, request, *args, **kwargs):
        athlete_id = request.data.get('athlete')
        coach_id = self.kwargs.get('id')

        coach = get_object_or_404(User, id=coach_id)
        athlete = User.objects.filter(id=athlete_id, is_staff=False)
        if not athlete.exists():
            return Response({"message": "athlete not found"}, status=status.HTTP_400_BAD_REQUEST)

        athlete = athlete.first()
        subscribe = Subscribe.objects.filter(athlete=athlete, coach=coach)
        if subscribe.exists():
            return Response({"message": "subscribe already exists"}, status=status.HTTP_400_BAD_REQUEST)

        Subscribe.objects.create(athlete=athlete, coach=coach)
        return Response({"message": "subscribe created successfully"}, status=status.HTTP_201_CREATED)
