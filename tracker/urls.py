"""Tracker URL configuration."""
from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("topic/<str:topic_id>/", views.topic_detail, name="topic_detail"),
    path("api/topic/<str:topic_id>/progress/", views.update_progress, name="update_progress"),
    path("api/topic/<str:topic_id>/notes/", views.add_notes, name="add_notes"),
    path("api/topic/<str:topic_id>/difficulty/", views.set_difficulty, name="set_difficulty"),
    path("api/overall/", views.overall_progress_api, name="overall_progress"),
]
