from email.policy import default
from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

# Create your models here.
class Job(models.Model):
    
    REQUEST_TYPE_CHOICES = (
        ("sync", "Sync"),
        ("async", "Async"),
    )

    JOB_TYPE_CHOICES = (
        ("image", "Image"),
        ("video", "Video"),
    )

    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("processed", "Processed"),
        ("sent", "Sent"),
        ("failed", "Failed"),
    )

    job_submitted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='job_submitted_by')
    title = models.CharField(max_length=255)
    request_type = models.CharField(default="async", choices=REQUEST_TYPE_CHOICES, max_length=32)
    added_at = models.DateTimeField(default=now, editable=False)
    job_type = models.CharField(default="image", choices = JOB_TYPE_CHOICES , max_length=32)
    status = models.CharField(default="pending", choices= STATUS_CHOICES, max_length=32)
    input_file = models.CharField(max_length=255, default="")
    out_email = models.CharField(max_length=255, default="", blank=True, null=True)
