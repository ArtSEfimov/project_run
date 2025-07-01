from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import User


class Run(models.Model):
    class Status(models.TextChoices):
        INIT = ("init", "Забег инициализирован")
        IN_PROGRESS = ("in_progress", "Забег начат")
        FINISHED = ("finished", "Забег закончен")

    created_at = models.DateTimeField(auto_now_add=True)
    comment = models.TextField()
    athlete = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.INIT)


class AthleteInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    goals = models.TextField(blank=True, default="")
    weight = models.IntegerField(blank=True, default=0, validators=[MinValueValidator(1), MaxValueValidator(899)])
