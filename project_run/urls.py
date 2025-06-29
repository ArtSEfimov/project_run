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

from app_run import views
from app_run.views import RunViewSet, UserViewSet, StartView, StopView

router = DefaultRouter()
router.register("api/runs", RunViewSet, basename="runs")
router.register("api/users", UserViewSet, basename="users")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/company_details/", views.company_info, name="company_info"),
    path("", include(router.urls)),
    path("api/runs/<int:run_id>/start/", StartView.as_view()),
    path("api/runs/<int:run_id>/stop/", StopView.as_view()),
]
