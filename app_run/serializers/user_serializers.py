from django.contrib.auth.models import User
from rest_framework import serializers

from .serializers import CollectibleItemSerializer


class PartialUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "last_name", "first_name")


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
        return obj.athlete_subscribes.values_list("coach_id", flat=True)
