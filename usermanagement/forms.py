from django import forms
from django.contrib.auth.forms import UserCreationForm
from wagtail.admin.forms import WagtailAdminModelForm
from usermanagement.models import CustomUser, UserProfile, CenterAdmin
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password


class UserWithProfileForm(WagtailAdminModelForm):
    username = forms.CharField()
    email = forms.EmailField()
    is_center_admin = forms.BooleanField()

    class Meta:
        model = UserProfile
        fields = (
            "username",
            "email",
            "is_center_admin",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # if instance is not None, it means we are editing an existing profile
        if self.instance and self.instance.user:
            self.fields["username"].initial = self.instance.user.username
            self.fields["email"].initial = self.instance.user.email
            self.fields["is_center_admin"].initial = self.instance.user.is_center_admin

    def save(self, commit=True):
        # save the profile first, as usual
        profile = super().save(commit=False)

        if self.instance.pk:  # editing an existing instance
            user = get_user_model().objects.get(pk=self.instance.user.pk)
            user.username = self.cleaned_data["username"]
            user.email = self.cleaned_data["email"]
            user.is_center_admin = self.cleaned_data["is_center_admin"]
            user.save()
        else:  # creating a new instance
            user = get_user_model().objects.create(
                username=self.cleaned_data["username"],
                email=self.cleaned_data["email"],
                is_center_admin=self.cleaned_data["is_center_admin"],
            )
            profile.user = user

        if commit:
            profile.save()

        return profile


class CenterAdminForm(forms.ModelForm):
    class Meta:
        model = CenterAdmin
        fields = "__all__"  # or specify fields here

    def save(self, commit=True):
        user = super().save(commit=False)
        user.password = make_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
