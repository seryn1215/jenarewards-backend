from rest_framework import serializers

from projects.models import Activity, Project
from usermanagement.models import UserProfile


class ActivitySerializer(serializers.ModelSerializer):

    project = serializers.SerializerMethodField(method_name="get_project")

    def get_project(self, obj):
        return ProjectSerializer(obj.project, context=self.context).data

    class Meta:
        model = Activity
        fields = ["id", "credited_coins", "joined_at", "project"]


class ProjectSerializer(serializers.ModelSerializer):
    activity_count = serializers.SerializerMethodField(method_name="get_activity_count")

    def get_activity_count(self, obj):
        user = self.context.get("user")
        if user is None:
            return 0
        profile = UserProfile.objects.get(user=user)
        print("user", user)
        print("project", obj)

        if profile is None:
            return 0

        activities = obj.activities.filter(user=profile)
        print("activities", activities)

        return activities.count()

    class Meta:
        model = Project

        fields = [
            "id",
            "name",
            "max_participants",
            "coins",
            "qr_code",
            "slug",
            "start_date",
            "end_date",
            "activity_count",
        ]
