from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Run, AthleteInfo, Challenge, Position, CollectibleItem, Subscribe
from .validators import latitude_validator, longitude_validator


class PartialUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "last_name", "first_name")


class CollectibleItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollectibleItem
        fields = "__all__"


class AthleteInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AthleteInfo
        fields = ("user_id", "goals", "weight")

    def get_user_id(self, obj):
        return obj.user__pk


class RunSerializer(serializers.ModelSerializer):
    athlete_data = PartialUserSerializer(source="athlete", read_only=True)
    athlete = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Run
        fields = "__all__"
        read_only_fields = ("status", "distance", "run_time_seconds", "speed")


class ChallengeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Challenge
        fields = ("athlete", "full_name")
        read_only_fields = ("full_name", "athlete")


_DATE_FORMAT = "%Y-%m-%dT%H:%M:%S.%f"


class PositionSerializer(serializers.ModelSerializer):
    date_time = serializers.DateTimeField(format=_DATE_FORMAT,
                                          input_formats=[_DATE_FORMAT])

    class Meta:
        model = Position
        fields = "__all__"
        read_only_fields = ("speed", "distance")
        extra_kwargs = {
            "latitude":
                {"validators": [latitude_validator],
                 },
            "longitude":
                {"validators": [longitude_validator],
                 },
        }

    def validate_run(self, run_object):
        if run_object.status == Run.Status.IN_PROGRESS:
            return run_object
        raise serializers.ValidationError("Забег должен быть только в статусе 'in_progress'")


class CollectibleItemValidator(serializers.ModelSerializer):
    url = serializers.URLField(source='picture')

    class Meta:
        model = CollectibleItem
        fields = ("name", "uid", "value", "latitude", "longitude", "url")

        extra_kwargs = {
            "latitude": {
                "validators": [latitude_validator],
            },
            "longitude": {
                "validators": [longitude_validator],
            },
        }


class FileUploadSerializer(serializers.Serializer):
    file = serializers.FileField(write_only=True, required=True)


class SubscribeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscribe
        fields = "__all__"


class UserListSerializer(PartialUserSerializer):
    type = serializers.SerializerMethodField(method_name="user_type")
    runs_finished = serializers.SerializerMethodField()

    class Meta(PartialUserSerializer.Meta):
        fields = PartialUserSerializer.Meta.fields + ("date_joined", "type", "runs_finished")

    def user_type(self, obj):
        return "coach" if obj.is_staff else "athlete"

    def get_runs_finished(self, obj):
        return obj.runs_finished


class UserDetailSerializer(UserListSerializer):
    items = CollectibleItemSerializer(many=True, read_only=True)

    class Meta(UserListSerializer.Meta):
        fields = UserListSerializer.Meta.fields + ("items",)

    def get_fields(self):
        fields = super().get_fields()
        user = self.context.get("user")
        if user.is_staff:
            fields["athletes"] = serializers.SerializerMethodField(read_only=True)
        else:
            fields["coach"] = serializers.SerializerMethodField(read_only=True)

        return fields

    def get_athletes(self, obj):
        return obj.coach_subscribes.values_list("athlete_id", flat=True)

    def get_coach(self, obj):
        coaches = obj.athlete_subscribes.all()
        if coaches.exists():
            return coaches.first().coach.pk

        return None
