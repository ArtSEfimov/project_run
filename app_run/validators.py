from rest_framework import serializers


def latitude_validator(value):
    if value < -90 or value > 90:
        raise serializers.ValidationError("Широта должна находиться в диапазоне от -90.0 до +90.0 градусов")
    return value


def longitude_validator(value):
    if value < -180 or value > 180:
        raise serializers.ValidationError("Долгота должна находиться в диапазоне от -180.0 до +180.0 градусов")
    return value
