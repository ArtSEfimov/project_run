from django.db.models import Count, Q
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.generics import get_object_or_404

from .models import Run, AthleteInfo, Challenge, Position


class PartialUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "last_name", "first_name")


class AthleteInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AthleteInfo
        fields = ("user_id", "goals", "weight")

    def get_user_id(self, obj):
        return obj.user__pk


class UserSerializer(PartialUserSerializer):
    type = serializers.SerializerMethodField(method_name="user_type")
    runs_finished = serializers.SerializerMethodField()

    class Meta(PartialUserSerializer.Meta):
        fields = PartialUserSerializer.Meta.fields + ("date_joined", "type", "runs_finished")

    def user_type(self, obj):
        return "coach" if obj.is_staff else "athlete"

    def get_runs_finished(self, obj):
        return obj.runs_finished


class RunSerializer(serializers.ModelSerializer):
    athlete_data = PartialUserSerializer(source="athlete", read_only=True)
    athlete = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.annotate(runs_finished=Count("run", filter=Q(run__status=Run.Status.FINISHED)))

    )

    class Meta:
        model = Run
        fields = "__all__"
        read_only_fields = ["status"]


class ChallengeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Challenge
        fields = ["full_name"]
        read_only_fields = ["full_name"]


class PositionSerializer(serializers.ModelSerializer):
    # run = serializers.PrimaryKeyRelatedField(
    #     queryset=Run.objects.all()
    # )

    class Meta:
        model = Position
        fields = "__all__"

    def validate_run(self, run_object):
        if run_object.status == Run.Status.IN_PROGRESS:
            return run_object
        raise serializers.ValidationError("Забег должен быть только в статусе 'in_progress'")

    def validate_latitude(self, value):
        if value < -90 or value > 90:
            raise serializers.ValidationError("Широта должна находиться в диапазоне от -90.0 до +90.0 градусов")
        return value

    def validate_longitude(self, value):
        if value < -180 or value > 180:
            raise serializers.ValidationError("Долгота должна находиться в диапазоне от -180.0 до +180.0 градусов")
        return value
