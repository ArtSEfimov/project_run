from django.forms import model_to_dict
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from .challenge_checkers import check_10_runs_challenge, check_50_km_challenge, check_2_km_in_10_minutes_challenge
from .stop_run_utils import get_distance, get_run_time, get_avg_speed
from ..models import Run


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

        # calculate distance
        run.distance = get_distance(run.pk)

        # calculate time
        run.run_time_seconds = get_run_time(run.pk)

        # calculate AVG speed
        run.speed = get_avg_speed(run.pk)

        run.save()

        # check 10 runs challenge
        check_10_runs_challenge(run.pk)

        # check 50 km challenge
        check_50_km_challenge(run.athlete.pk)

        # check 2 km in 10 minutes challenge
        check_2_km_in_10_minutes_challenge(run)

        return Response(model_to_dict(run), status=status.HTTP_200_OK)
