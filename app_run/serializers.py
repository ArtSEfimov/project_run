from rest_framework import serializers
from django.contrib.auth.models import User
from app_run.models import Run


class PartialUserSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField(method_name='user_type')

    class Meta:
        model = User
        fields = ('id', 'username', 'last_name', 'first_name', 'type')

    def user_type(self, obj):
        return "coach" if obj.is_staff else "athlete"


class UserSerializer(PartialUserSerializer):
    class Meta(PartialUserSerializer.Meta):
        fields = PartialUserSerializer.Meta.fields + ('date_joined',)


class RunSerializer(serializers.ModelSerializer):
    athlete_data = PartialUserSerializer(source='athlete', read_only=True)
    athlete = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        write_only=True,
    )

    class Meta:
        model = Run
        fields = '__all__'
