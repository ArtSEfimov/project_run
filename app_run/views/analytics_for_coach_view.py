from django.contrib.auth.models import User
from rest_framework.views import APIView


class AnalyticsForCoachViewSet(APIView):
    def get(self, request, coach_id):
        pass

    def get_queryset(self):
        coach_id = self.kwargs.get('coach_id')

        coaches_queryset = (
            User.objects.filter(is_staff=True, id=coach_id)
            .prefetch_related("coach_subscribes__athlete__run_set")
        )
