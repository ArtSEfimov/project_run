from functools import cached_property

from django_filters.rest_framework import DjangoFilterBackend
from haversine import Unit, haversine
from rest_framework.viewsets import ModelViewSet

from ..models import Position, CollectibleItem
from ..serializers.serializers import PositionSerializer


class PositionView(ModelViewSet):
    queryset = Position.objects.select_related("run").all()
    serializer_class = PositionSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["run"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.run_object = None

    @cached_property
    def collectible_items_queryset(self):
        return CollectibleItem.objects.all()

    def perform_create(self, serializer):
        self.run_object = serializer.validated_data["run"]
        speed = self.calculate_speed(serializer)
        distance = self.get_overall_distance(serializer)
        position_instance = serializer.save(speed=speed, distance=distance)
        self.check_nearby_items(position_instance)

    def perform_update(self, serializer):
        self.run_object = serializer.validated_data["run"]
        speed = self.calculate_speed(serializer)
        distance = self.get_overall_distance(serializer)
        position_instance = serializer.save(speed=speed, distance=distance)
        self.check_nearby_items(position_instance)

    def check_nearby_items(self, position_instance):
        for item in self.collectible_items_queryset:
            user_position = position_instance.latitude, position_instance.longitude
            item_position = item.latitude, item.longitude
            if haversine(user_position, item_position, unit=Unit.METERS) <= 100:
                item.users.add(position_instance.run.athlete)

    def calculate_distance(self, serializer):
        current_point_latitude = serializer.validated_data["latitude"]
        current_point_longitude = serializer.validated_data["longitude"]
        current_position = current_point_latitude, current_point_longitude

        previous_point = self._previous_position
        if not previous_point:
            return 0

        previous_position = previous_point.latitude, previous_point.longitude

        return haversine(current_position, previous_position, unit=Unit.KILOMETERS)

    def get_overall_distance(self, serializer):
        distance = self.calculate_distance(serializer)
        previous_point = self._previous_position
        if not previous_point:
            return distance
        return distance + previous_point.distance

    def calculate_speed(self, serializer):
        current_point_date_time = serializer.validated_data["date_time"]

        previous_point = self._previous_position
        if not previous_point:
            return 0

        time_delta_seconds = (current_point_date_time - previous_point.date_time).seconds

        return round((self.calculate_distance(serializer) * 1000) / time_delta_seconds, 2)

    @cached_property
    def _previous_position(self) -> Position | None:
        points = Position.objects.filter(run=self.run_object)
        if points:
            previous_point = points.latest("date_time")
            return previous_point

        return None
