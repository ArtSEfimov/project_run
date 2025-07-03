from functools import cached_property

from django_filters.rest_framework import DjangoFilterBackend
from haversine import haversine, Unit
from rest_framework.viewsets import ModelViewSet

from ..models import Position, CollectibleItem
from ..serializers import PositionSerializer


class PositionView(ModelViewSet):
    queryset = Position.objects.select_related("run").all()
    serializer_class = PositionSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["run"]

    @cached_property
    def collectible_items_queryset(self):
        return CollectibleItem.objects.all()

    def perform_create(self, serializer):
        run_instance = serializer.save()
        self.check_nearby_items(run_instance)

    def perform_update(self, serializer):
        run_instance = serializer.save()
        self.check_nearby_items(run_instance)

    def check_nearby_items(self, run_instance):
        for item in self.collectible_items_queryset():
            start = run_instance.latitude, run_instance.longitude
            finish = item.latitude, item.longitude
            if haversine(start, finish, unit=Unit.METERS) <= 100:
                item.users.add(run_instance.athlete)
