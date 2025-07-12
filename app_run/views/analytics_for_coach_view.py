from django.contrib.auth.models import User
from django.db.models import Max, Sum, Avg
from django.http import JsonResponse
from rest_framework import status
from rest_framework.views import APIView


class AnalyticsForCoachViewSet(APIView):
    def get(self, request, coach_id):
        athletes = (
            User.objects.filter(athlete_subscribes__coach=coach_id)
            .annotate(max_distance=Max("run__distance"))
            .annotate(sum_distance=Sum("run__distance"))
            .annotate(avg_speed=Avg("run__speed"))
        )

        max_distance_athlete = max(
            athletes, key=lambda a: a.max_distance
        )
        sum_distance_athlete = max(
            athletes, key=lambda a: a.sum_distance
        )
        avg_speed_athlete = max(
            athletes, key=lambda a: a.avg_speed
        )

        response = {
            'longest_run_user': max_distance_athlete.pk,  # Id Бегуна, который сделал самый длинный забег у этого Тренера

            'longest_run_value': max_distance_athlete.msx_distance,  # Дистанция самого длинного забега

            'total_run_user': sum_distance_athlete.pk,  # Id Бегуна, который пробежал в сумме больше всех у этого Тренера

            'total_run_value': sum_distance_athlete.sum_distance,  # Дистанция которую в сумме пробежал этот Бегун

            'speed_avg_user': avg_speed_athlete.pk,  # Id Бегуна который в среднем бежал быстрее всех

            'speed_avg_value': avg_speed_athlete.avg_speed,  # Средняя скорость этого Бегуна
        }

        return JsonResponse(data=response, status=status.HTTP_200_OK)
