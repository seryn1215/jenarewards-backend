from typing import Any
from django.shortcuts import render
from django.views.generic import TemplateView

from dashboard.models import PrivacyPolicyPage


# Create your views here.
class PrivacyPolicyPageView(TemplateView):
    template_name = "dashboard/privacy.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page"] = PrivacyPolicyPage.objects.first()
        print("content", context["page"].content)
        print("title", context["page"].title)
        print("context", context)

        return context
