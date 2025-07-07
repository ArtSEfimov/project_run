from django.core.cache import cache
from django.db.models import Min, Max, Avg
from haversine import haversine

from ..models import Position

_CACHE_TIMEOUT = 60


def get_cached_points(run_id):
    key = f"{run_id}_point_set"
    points = cache.get(key, None)
    if points is None:
        points = Position.objects.filter(run=run_id)
        if points.exists():
            cache.set(key, points, timeout=_CACHE_TIMEOUT)

    return points


def get_distance(run_id):
    points = get_cached_points(run_id)
    distance = 0
    for i in range(len(points) - 1):
        start = points[i].latitude, points[i].longitude
        finish = points[i + 1].latitude, points[i + 1].longitude
        distance += haversine(start, finish)

    return distance


def get_run_time(run_id):
    points = get_cached_points(run_id)
    if points.exists():
        timestamps = points.aggregate(min_time=Min("date_time"),
                                      max_time=Max("date_time"))

        start_time = timestamps["min_time"]
        finish_time = timestamps["max_time"]

        return (finish_time - start_time).seconds

    return 0


def get_avg_speed(run_id):
    points = get_cached_points(run_id)
    if points.exists():
        return points.aggregate(avg_speed=Avg("speed"))["avg_speed"]

    return 0
