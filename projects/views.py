from django.shortcuts import render
import pytz

from projects.models import Activity, Project
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from knox.models import AuthToken
from knox.settings import CONSTANTS
from projects.serializer import ActivitySerializer, ProjectSerializer
import datetime
from usermanagement.models import User, UserProfile


# Create your views here.
def projects(request):
    projects = Project.objects.all()
    return render(request, "projects/project_list.html", {"projects": projects})


def project_detail(request, slug):
    project = Project.objects.get(slug=slug)
    return render(request, "projects/project_detail.html", {"project": project})


@api_view(["GET"])
def add_user_to_project(request, project_slug):
    knox_token = request.headers.get("Authorization").split(" ")[1]

    uid = AuthToken.objects.get(
        token_key=knox_token[: CONSTANTS.TOKEN_KEY_LENGTH]
    ).user.uid

    user = User.objects.get(uid=uid)
    profile = UserProfile.objects.get(user=user)

    project = Project.objects.get(slug=project_slug)

    if project.participants.filter(pk=profile.pk).exists():
        return Response(
            {"error": "User already added to project"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if project.participants.count() >= project.max_participants:
        return Response(
            {"error": "Project is full"}, status=status.HTTP_400_BAD_REQUEST
        )

    project.participants.add(profile)

    return Response({"detail": "User added to project"}, status=status.HTTP_200_OK)


@api_view(["GET"])
# @permission_classes([IsAuthenticated])
def add_user_to_project_activity(request, pk):
    try:
        print("add_user_to_project_activity-request.user", request.user)
        time_zone = request.GET.get("timezone")
        date = datetime.datetime.now(pytz.timezone(time_zone))

        if time_zone not in pytz.all_timezones:
            return Response({"error": "Invalid timezone"}, status=400)

        knox_token = request.headers.get("Authorization").split(" ")[1]

        uid = AuthToken.objects.get(
            token_key=knox_token[: CONSTANTS.TOKEN_KEY_LENGTH]
        ).user.uid

        user = User.objects.get(uid=uid)
        profile = UserProfile.objects.get(user=user)

        project = Project.objects.get(pk=pk)

        print("project", project)

        if not project.participants.filter(pk=profile.pk).exists():
            return Response(
                {"error": "User is not a participant of this project"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # check if project allows participants to join in this timestamp based on day
        current_time = date.time()
        current_day = date.strftime("%a").lower()

        print("current_time", current_time)
        print("current_day", current_day)

        is_day_selected = getattr(project, current_day)
        print("is_day_selected", is_day_selected)
        start_time = getattr(project, current_day + "_start_time")
        print("start_time", start_time)
        end_time = getattr(project, current_day + "_end_time")
        print("end_time", end_time)

        if not is_day_selected:
            return Response(
                {"error": "Project not available on this day"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if (start_time and end_time) and (
            current_time < start_time or current_time > end_time
        ):
            return Response(
                {"error": "Project not available at this time"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        curerent_date = date.date()

        # check if user already has activity for today
        activities = project.activities.filter(
            user=profile, joined_at__date=curerent_date
        )

        if (
            project.max_activity_per_day
            and activities.count() >= project.max_activity_per_day
        ):
            return Response(
                {"error": "User already has maximum activities for today"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # create activity
        activity = Activity.objects.create(
            project=project, user=profile, credited_coins=project.coins
        )
        activity.save()

        project.save()

        return Response({"detail": "User added to project"}, status=status.HTTP_200_OK)
    except Project.DoesNotExist:
        return Response(
            {"error": "Project not found"}, status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        import traceback

        traceback.print_exc()
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
# @permission_classes([IsAuthenticated])
def get_all_user_projects(request):
    try:
        knox_token = request.headers.get("Authorization").split(" ")[1]

        uid = AuthToken.objects.get(
            token_key=knox_token[: CONSTANTS.TOKEN_KEY_LENGTH]
        ).user.uid

        user = User.objects.get(uid=uid)
        profile = UserProfile.objects.get(user=user)
        projects = Project.objects.filter(participants=profile)
        # serialize
        print("projects", projects)
        serializer = ProjectSerializer(projects, many=True, context={"user": user})
        print("serializer.data", serializer.data)
        return Response({"projects": serializer.data}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
# @permission_classes([IsAuthenticated])
def get_all_user_project_activities(request, project_slug):
    try:
        knox_token = request.headers.get("Authorization").split(" ")[1]

        uid = AuthToken.objects.get(
            token_key=knox_token[: CONSTANTS.TOKEN_KEY_LENGTH]
        ).user.uid

        user = User.objects.get(uid=uid)
        profile = UserProfile.objects.get(user=user)
        project = Project.objects.get(slug=project_slug)
        activities = project.activities.filter(user=profile)

        serializer = ActivitySerializer(activities, many=True, context={"user": user})

        return Response({"activities": serializer.data}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


def qr_code_view(request, slug):
    project = Project.objects.get(slug=slug)
    return render(request, "projects/qr_code.html", {"project": project})


def activity_code_view(request, pk):
    project = Project.objects.get(pk=pk)
    return render(request, "projects/activity_code.html", {"project": project})


@api_view(["GET"])
def remove_user_from_project(request, project_slug):
    knox_token = request.headers.get("Authorization").split(" ")[1]

    uid = AuthToken.objects.get(
        token_key=knox_token[: CONSTANTS.TOKEN_KEY_LENGTH]
    ).user.uid

    user = User.objects.get(uid=uid)
    profile = UserProfile.objects.get(user=user)

    project = Project.objects.get(slug=project_slug)

    # profile.coins -= project.coins
    profile.save()

    project.participants.remove(profile)
    project.save()

    return Response({"detail": "User removed from project"}, status=status.HTTP_200_OK)


@api_view(["GET"])
def get_user_activities(request):
    knox_token = request.headers.get("Authorization").split(" ")[1]

    uid = AuthToken.objects.get(
        token_key=knox_token[: CONSTANTS.TOKEN_KEY_LENGTH]
    ).user.uid

    user = User.objects.get(uid=uid)
    print("user", user)
    profile = UserProfile.objects.get(user=user)
    print("profile", profile)

    activities = Activity.objects.filter(user=profile)

    serializer = ActivitySerializer(activities, many=True, context={"user": user})

    return Response({"activities": serializer.data}, status=status.HTTP_200_OK)
