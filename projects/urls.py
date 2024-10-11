from django.urls import path
from . import views

urlpatterns = [
    path("", views.get_all_user_projects, name="projects"),
    # path("<int:project_id>/", views.project_detail, name="project_detail"),
    # path for the project detail page with slug
    path("<str:slug>/", views.project_detail, name="project_detail"),
    path("<str:project_slug>/join", views.add_user_to_project, name="join_user"),
    path("<str:project_slug>/leave", views.remove_user_from_project, name="leave_user"),
    path("qr_code/<str:slug>/", views.qr_code_view, name="qr_code"),
    path("activity_code/<str:pk>/", views.activity_code_view, name="activity_code"),
    path(
        "<str:project_slug>/activities/",
        views.get_all_user_project_activities,
        name="user_project_activities",
    ),
    path(
        "activities/<int:pk>/join",
        views.add_user_to_project_activity,
        name="activity_join_user",
    ),
    path("activities/me", views.get_user_activities, name="user_activities"),
]
