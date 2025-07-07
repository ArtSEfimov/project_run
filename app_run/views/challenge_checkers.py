from django.db.models import Sum

from .views import UserAnnotatedQuerySet
from ..models import Challenge, Run

_CHALLENGE_10_RUNS = "Сделай 10 Забегов!"
_10_RUNS = 10


def check_10_runs_challenge(run_id):
    user = UserAnnotatedQuerySet.queryset.get(run=run_id)
    if user.runs_finished % _10_RUNS == 0:
        Challenge.objects.create(full_name=_CHALLENGE_10_RUNS, athlete=user)


_CHALLENGE_50_KM = "Пробеги 50 километров!"
_50_KM = 50


def check_50_km_challenge(user_id):
    user_distance = Run.objects.filter(athlete=user_id).aggregate(total_distance=Sum("distance"))
    if user_distance["total_distance"] >= _50_KM:
        Challenge.objects.get_or_create(full_name=_CHALLENGE_50_KM, athlete_id=user_id)


_CHALLENGE_2_KM_IN_10_MINUTES = "2 километра за 10 минут!"
_2_KM = 2
_10_MINUTES_IN_SECONDS = 600


def check_2_km_in_10_minutes_challenge(run):
    if run.distance >= _2_KM and run.run_time_seconds <= _10_MINUTES_IN_SECONDS:
        Challenge.objects.get_or_create(full_name=_CHALLENGE_2_KM_IN_10_MINUTES, athlete_id=run.athlete.pk)
