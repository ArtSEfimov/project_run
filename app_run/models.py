from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Run(models.Model):
    class Status(models.TextChoices):
        INIT = ("init", "Забег инициализирован")
        IN_PROGRESS = ("in_progress", "Забег начат")
        FINISHED = ("finished", "Забег закончен")

    created_at = models.DateTimeField(auto_now_add=True)
    comment = models.TextField()
    athlete = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.INIT)
    distance = models.FloatField(default=0, blank=True, null=True)
    # run_time_seconds = models.DateTimeField(default=0)


class AthleteInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    goals = models.TextField(blank=True, default="")
    weight = models.IntegerField(blank=True, default=0, validators=[MinValueValidator(1), MaxValueValidator(899)])


class Challenge(models.Model):
    full_name = models.CharField(max_length=50)
    athlete = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="challenges",
                                related_query_name="query_challenges")


class Position(models.Model):
    run = models.ForeignKey(Run, on_delete=models.CASCADE)
    latitude = models.DecimalField(default=0, decimal_places=4, max_digits=6)
    longitude = models.DecimalField(default=0, decimal_places=4, max_digits=7)
    # date_time = models.DateTimeField(auto_now_add=True)


class CollectibleItem(models.Model):
    name = models.CharField(max_length=50)
    uid = models.CharField(max_length=50)
    latitude = models.DecimalField(default=0, decimal_places=4, max_digits=6)
    longitude = models.DecimalField(default=0, decimal_places=4, max_digits=7)
    picture = models.URLField()
    value = models.IntegerField()
    # users = models.ManyToManyField(User, blank=True, related_name="items", related_query_name="query_items")
