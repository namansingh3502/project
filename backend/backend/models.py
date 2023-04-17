from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserProfile(AbstractUser):
    """
    Only required columns are added.
    Already Present
        username, password, first_name, last_name, email, is_active,
        is_staff, is_superuser, last_login, date_joined
    Additional Details
        prefix, middle_name, phone
    """

    phone = models.CharField(
        _("Mobile No."),
        max_length=10
    )
    is2faActivated = models.BooleanField(default=False, null=False, blank=False)

    AbstractUser._meta.get_field('first_name').blank = False
    AbstractUser._meta.get_field('first_name').null = False
    AbstractUser._meta.get_field('last_name').blank = False
    AbstractUser._meta.get_field('last_name').null = False
    AbstractUser._meta.get_field('email').blank = False
    AbstractUser._meta.get_field('email').null = False

    class Meta:
        db_table = "User_Profile"

    def __str__(self):
        return self.username


class UserTOTPDetails(models.Model):
    user = models.ForeignKey(
        'UserProfile',
        on_delete=models.CASCADE
    )
    platform = models.CharField(
        "Platform",
        max_length=50,
        blank=False,
        null=False,
    )
    delay = models.IntegerField(
        "Time delay",
        blank=False,
        null=False
    )
    key = models.CharField(
        "Key",
        max_length=128,
        blank=True,
        null=False
    )

    class Meta:
        db_table = "UserTOTPDetails"
        unique_together = ('user', 'platform')
