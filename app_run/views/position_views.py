from functools import cached_property

from django.db.models import Sum
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
        speed = self.calculate_speed(serializer)
        distance = self.calculate_distance(serializer) + self.get_overall_distance()
        position_instance = serializer.save(speed=speed, distance=distance)
        self.check_nearby_items(position_instance)

    def perform_update(self, serializer):
        speed = self.calculate_speed(serializer)
        distance = self.calculate_distance(serializer) + self.get_overall_distance()
        position_instance = serializer.save(speed=speed, distance=distance)
        self.check_nearby_items(position_instance)

    def check_nearby_items(self, position_instance):
        for item in self.collectible_items_queryset:
            user_position = position_instance.latitude, position_instance.longitude
            item_position = item.latitude, item.longitude
            if haversine(user_position, item_position, unit=Unit.METERS) <= 100:
                item.users.add(position_instance.run.athlete)

    def get_overall_distance(self):
        return self.queryset.aggregate(distance=Sum("distance"))["distance"]

    def calculate_distance(self, serializer):
        current_point_latitude = serializer.validated_data["latitude"]
        current_point_longitude = serializer.validated_data["longitude"]
        current_position = current_point_latitude, current_point_longitude

        previous_point, is_exists = self.get_previous_position()
        if not is_exists:
            return 0

        previous_position = previous_point.latitude, previous_point.longitude

        return haversine(current_position, previous_position, unit=Unit.METERS)

    def calculate_speed(self, serializer):
        current_point_date_time = serializer.validated_data["date_time"]

        previous_point, is_exists = self.get_previous_position()
        if not is_exists:
            return 0

        time_delta_seconds = (current_point_date_time - previous_point.date_time).seconds

        return round(self.calculate_distance(serializer) / time_delta_seconds, 2)

    def get_previous_position(self) -> (Position, bool):
        if self.queryset.exists():
            point = self.queryset.latest("date_time")
            return point, True
        return None, False
