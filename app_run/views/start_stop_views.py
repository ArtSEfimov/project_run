from django.forms import model_to_dict
from haversine import haversine
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from .user_views import UserAnnotatedQuerySet
from ..models import Run, Challenge, Position


class StartView(APIView):
    def post(self, request, run_id):
        run = get_object_or_404(Run, id=run_id)
        print(run.status)
        if run.status in (Run.Status.FINISHED, Run.Status.IN_PROGRESS):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        run.status = Run.Status.IN_PROGRESS
        run.save()

        return Response(model_to_dict(run), status=status.HTTP_200_OK)


class StopView(APIView):
    def post(self, request, run_id):
        run = get_object_or_404(Run, id=run_id)
        if run.status != Run.Status.IN_PROGRESS:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        run.status = Run.Status.FINISHED

        # check challenge
        get_challenge(run.pk)

        # calculate distance
        run.distance = get_distance(run.pk)

        run.save()
        return Response(model_to_dict(run), status=status.HTTP_200_OK)


def get_challenge(run_id):
    user = UserAnnotatedQuerySet.queryset.get(run=run_id)
    if user.runs_finished % 10 == 0:
        Challenge.objects.create(full_name="Сделай 10 Забегов!",
                                 athlete=user)


def get_distance(run_id):
    points = Position.objects.filter(run=run_id)
    distance = 0
    for i in range(len(points) - 1):
        start = points[i].latitude, points[i].longitude
        finish = points[i + 1].latitude, points[i + 1].longitude
        distance += haversine(start, finish)

    return distance
