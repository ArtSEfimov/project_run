from django.db.models import Sum
from haversine import haversine

from ..models import Challenge, Position, Run
from ..views.user_views import UserAnnotatedQuerySet

_CHALLENGE_10_RUNS = "Сделай 10 Забегов!"
_CHALLENGE_50_KM = "Пробеги 50 километров!"


def check_10_runs_challenge(run_id):
    user = UserAnnotatedQuerySet.queryset.get(run=run_id)
    if user.runs_finished % 10 == 0:
        Challenge.objects.create(full_name=_CHALLENGE_10_RUNS, athlete=user)


def check_50_km_challenge(user_id):
    user_distance = Run.objects.filter(athlete=user_id).aggregate(total_distance=Sum("distance"))
    if user_distance["total_distance"] >= 50:
        Challenge.objects.get_or_create(full_name=_CHALLENGE_50_KM, athlete_id=user_id)


def get_distance(run_id):
    points = Position.objects.filter(run=run_id)
    distance = 0
    for i in range(len(points) - 1):
        start = points[i].latitude, points[i].longitude
        finish = points[i + 1].latitude, points[i + 1].longitude
        distance += haversine(start, finish)

    return distance


def get_run_time(run_id):
    pass
