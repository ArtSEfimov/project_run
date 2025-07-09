"""
URL configuration for project_run project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from app_run.views.challenge_view import get_challenge_info
from app_run.views.collectible_items_view import CollectibleItemView, UploadFileView
from app_run.views.position_views import PositionView
from app_run.views.run_views import RunViewSet
from app_run.views.start_stop_views import StartView, StopView
from app_run.views.subscribe_view import SubscribeCreateView
from app_run.views.user_views import UserViewSet, AthleteInfoView
from app_run.views.views import company_info

router = DefaultRouter()
router.register("api/runs", RunViewSet, basename="runs")
router.register("api/users", UserViewSet, basename="users")
router.register("api/positions", PositionView, basename="position")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/company_details/", company_info, name="company_info"),
    path("", include(router.urls)),
    path("api/runs/<int:run_id>/start/", StartView.as_view(), name="start_run"),
    path("api/runs/<int:run_id>/stop/", StopView.as_view(), name="stop_run"),
    path("api/athlete_info/<int:user_id>/", AthleteInfoView.as_view(), name="athlete_info"),
    path("api/challenges/", get_challenge_info, name="challenge_info"),
    path("api/collectible_item/", CollectibleItemView.as_view(), name="collectible_item"),
    path("api/upload_file/", UploadFileView.as_view(), name="upload_file"),
    path("api/subscribe_to_coach/<int:id>/", SubscribeCreateView.as_view(), name="subscribe_to_coach"),
]
