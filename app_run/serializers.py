from rest_framework import serializers
from django.contrib.auth.models import User
from app_run.models import Run, AthleteInfo, Challenge


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
        queryset=User.objects.all()
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
