from django.urls import path
from . import views

urlpatterns = [
    path(
        "privacy-policy/", views.PrivacyPolicyPageView.as_view(), name="privacy-policy"
    )
]
