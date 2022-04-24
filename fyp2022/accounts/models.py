from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

class UserProfile(models.Model):

    TYPE_CHOICES = (
        ("superadmin", "Super Admin"),
        ("customer", "Customer"),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='related_user')
    type = models.CharField(default="superadmin", choices=TYPE_CHOICES, max_length=32)
    added_by = models.ForeignKey( User,default=1, on_delete=models.CASCADE, related_name='user_added_by')
    added_at = models.DateTimeField(default=now, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"user: {self.user.username}, type: {self.type}, added by: {self.added_by}"

User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])