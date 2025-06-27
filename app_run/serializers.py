from rest_framework.serializers import ModelSerializer, SerializerMethodField
from django.contrib.auth.models import User
from app_run.models import Run


class UserSerializer(ModelSerializer):
    type = SerializerMethodField(method_name='user_type')

    class Meta:
        model = User
        fields = ('id', 'date_joined', 'username', 'last_name', 'first_name', 'type')

    def user_type(self, obj):
        return "coach" if obj.is_staff else "athlete"

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)
        super().__init__(*args, **kwargs)
        if fields is not None:
            method_fields = {
                name
                for name, field in self.fields.items()
                if isinstance(field, SerializerMethodField)
            }
            allowed_fields = set(fields).union(method_fields)
            forbidden_fields = set(self.fields).difference(allowed_fields)
            for filed in forbidden_fields:
                self.fields.pop(filed)


class RunSerializer(ModelSerializer):
    athlete_data = UserSerializer(source='athlete', read_only=True,
                                  fields=('id', 'username', 'last_name', 'first_name'))

    class Meta:
        model = Run
        exclude = ('athlete',)
