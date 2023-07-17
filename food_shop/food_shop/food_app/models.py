from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth import models as auth_models


def is_old_enough(value):
    if value < 12:
        raise ValidationError('You have to be at least 12 years old to use this app!')


# Create your models here.
class CustomUser(auth_models.AbstractUser):
    age = models.PositiveIntegerField(
        null=False,
        blank=False,
        validators=[is_old_enough]
    )

    first_name = models.CharField(
        blank=True,
        null=True,
        max_length=20
    )
    last_name = models.CharField(
        blank=True,
        null=True,
        max_length=20
    )

    birth_date = models.DateField(
        blank=True,
        null=True,
    )

    profile_picture = models.URLField(
        blank=True,
        null=True
    )

    bio = models.TextField(
        blank=True,
        null=True,
        max_length=250
    )
