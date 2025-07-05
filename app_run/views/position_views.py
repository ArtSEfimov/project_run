from functools import cached_property

from django_filters.rest_framework import DjangoFilterBackend
from haversine import Unit, haversine

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
        position_instance = serializer.save()
        self.check_nearby_items(position_instance)

    def perform_update(self, serializer):
        position_instance = serializer.save()
        self.check_nearby_items(position_instance)

    def check_nearby_items(self, position_instance):
        for item in self.collectible_items_queryset:
            user_position = position_instance.latitude, position_instance.longitude
            item_position = item.latitude, item.longitude
            if haversine(user_position, item_position, unit=Unit.METERS) <= 100:
                item.users.add(position_instance.run.athlete)
