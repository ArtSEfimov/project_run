from django.forms import model_to_dict
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from .user_views import UserAnnotatedQuerySet
from ..models import Run, Challenge


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
        run.save()
        user = UserAnnotatedQuerySet.queryset.get(run=run)
        if user.runs_finished == 10:
            Challenge.objects.create(full_name="Сделай 10 Забегов!",
                                     athlete=user)

        return Response(model_to_dict(run), status=status.HTTP_200_OK)

