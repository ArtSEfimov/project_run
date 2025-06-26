from rest_framework.serializers import ModelSerializer, SerializerMethodField
from django.contrib.auth.models import User
from app_run.models import Run


class RunSerializer(ModelSerializer):
    class Meta:
        model = Run
        fields = '__all__'


class UserSerializer(ModelSerializer):
    type = SerializerMethodField(method_name='user_type')

    class Meta:
        model = User
        fields = ('id', 'date_joined', 'username', 'last_name', 'first_name', 'type')

    def user_type(self, obj):
        return "coach" if obj.is_staff else "athlete"
