from django.urls import path

from usermanagement.views import (
    FirebaseLoginView,
    FirebaseLogoutView,
    LoginView,
    UserView,
)

urlpatterns = [
    path("login", LoginView.as_view(), name="login"),
    path("firebase-login", FirebaseLoginView.as_view(), name="firebase-login"),
    path("logout", FirebaseLogoutView.as_view(), name="logout"),
    path("me", UserView.as_view(), name="me"),
]
