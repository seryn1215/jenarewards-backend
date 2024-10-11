from django.db import models

from django.db import models
from django.utils.text import slugify
from usermanagement.models import CustomUser, UserProfile
import qrcode
from PIL import Image, ImageDraw
from django.core.files import File
from io import BytesIO
from django.urls import reverse
from wagtail.admin.panels import FieldPanel, MultiFieldPanel


class Project(models.Model):
    name = models.CharField(max_length=255)
    center_admins = models.ManyToManyField(
        CustomUser, limit_choices_to={"is_center_admin": True}, related_name="projects"
    )
    max_participants = models.PositiveIntegerField()
    participants = models.ManyToManyField(
        UserProfile, related_name="projects", blank=True
    )
    qr_code = models.ImageField(upload_to="qr_codes/", blank=True, null=True)
    activity_code = models.ImageField(
        upload_to="activity_codes/", blank=True, null=True
    )
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    start_date = models.DateTimeField(
        default=None,
    )
    end_date = models.DateTimeField(
        default=None,
    )

    max_activity_per_day = models.PositiveIntegerField(null=True, default=1)

    coins = models.PositiveIntegerField(null=True, default=0)

    mon = models.BooleanField(null=True, default=False)
    mon_start_time = models.TimeField(null=True, blank=True)
    mon_end_time = models.TimeField(null=True, blank=True)

    tue = models.BooleanField(null=True, default=False)
    tue_start_time = models.TimeField(null=True, blank=True)
    tue_end_time = models.TimeField(null=True, blank=True)

    wed = models.BooleanField(null=True, default=False)
    wed_start_time = models.TimeField(null=True, blank=True)
    wed_end_time = models.TimeField(null=True, blank=True)

    thu = models.BooleanField(null=True, default=False)
    thu_start_time = models.TimeField(null=True, blank=True)
    thu_end_time = models.TimeField(null=True, blank=True)

    fri = models.BooleanField(null=True, default=False)
    fri_start_time = models.TimeField(null=True, blank=True)
    fri_end_time = models.TimeField(null=True, blank=True)

    sat = models.BooleanField(null=True, default=False)
    sat_start_time = models.TimeField(null=True, blank=True)
    sat_end_time = models.TimeField(null=True, blank=True)

    sun = models.BooleanField(null=True, default=False)
    sun_start_time = models.TimeField(null=True, blank=True)
    sun_end_time = models.TimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            # Generate slug
            value = self.name
            slug_candidate = slugify(value, allow_unicode=True)
            self.slug = self.generate_unique_slug(slug_candidate)

        super().save(*args, **kwargs)

        # # Generate and save QR code image after the model is saved
        # if not self.qr_code:
        #     self.generate_qr_code()

    def generate_unique_slug(self, slug_candidate):
        unique_slug = slug_candidate
        num = 1
        while Project.objects.filter(slug=unique_slug).exists():
            num += 1
            unique_slug = "{}-{}".format(slug_candidate, num)
        return unique_slug

    def generate_qr_code(self):
        # Create qr code instance
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        data = "join_project:{}".format(self.slug)

        qr.add_data(data)
        qr.make(fit=True)

        img = qr.make_image(fill="black", back_color="white")
        temp = BytesIO()
        img.save(temp, format="PNG")
        temp.seek(0)

        file_name = f"qr_code-{self.slug}.png"
        self.qr_code.save(file_name, File(temp), save=True)

    def generate_activity_code(self):
        # Create qr code instance
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )

        data = "activity_code:{}".format(self.pk)

        qr.add_data(data)
        qr.make(fit=True)

        img = qr.make_image(fill="black", back_color="white")
        temp = BytesIO()
        img.save(temp, format="PNG")
        temp.seek(0)

        file_name = f"{data}.png"
        self.activity_code.save(file_name, File(temp), save=True)

    def get_absolute_url(self):
        return reverse("project_detail", args=[str(self.slug)])

    def __str__(self):
        return self.name

    @classmethod
    def get_edit_handler(cls):
        panels = (
            [
                FieldPanel("name"),
                FieldPanel("max_participants"),
                FieldPanel("start_date"),
                FieldPanel("end_date"),
                FieldPanel("mon_start_time", heading="Monday"),
                FieldPanel("mon_end_time"),
                FieldPanel("tue_start_time"),
                FieldPanel("tue_end_time"),
                FieldPanel("wed_start_time"),
                FieldPanel("wed_end_time"),
                FieldPanel("thu_start_time"),
                FieldPanel("thu_end_time"),
                FieldPanel("fri_start_time"),
                FieldPanel("fri_end_time"),
                FieldPanel("sat_start_time"),
                FieldPanel("sat_end_time"),
                FieldPanel("sun_start_time"),
                FieldPanel("sun_end_time"),
            ],
        )

        edit_handler = MultiFieldPanel(panels, heading="Project")
        return edit_handler.bind_to_model(cls)


class Activity(models.Model):
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="activities"
    )
    user = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name="activities"
    )
    credited_coins = models.PositiveIntegerField(default=0)
    joined_at = models.DateTimeField(auto_now_add=True)
