from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel


# Create your models here.
class PrivacyPolicyPage(Page):
    content = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("content", classname="full"),
    ]

    parent_page_types = ["home.HomePage"]

    template = "dashboard/privacy.html"
