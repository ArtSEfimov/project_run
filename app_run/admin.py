from django.contrib import admin

from .models import Run, AthleteInfo, Position, Challenge, CollectibleItem

# Register your models here.
admin.site.register(Run)
admin.site.register(AthleteInfo)
admin.site.register(Position)
admin.site.register(Challenge)
admin.site.register(CollectibleItem)
