from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth import models as auth_models, get_user_model
from django.conf import settings
from django.db.models.signals import pre_save
from django.dispatch import receiver


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


class Recipe(models.Model):
    CHOICES = (
        ('hot', 'hot'),
        ('cold', 'cold'),
        ('frozen', 'frozen'),
    )

    title = models.CharField(
        max_length=50,
        null=False,
        blank=False
    )
    description = models.TextField(
        null=False,
        blank=False
    )
    ingredients = models.TextField(
        null=False,
        blank=False
    )
    instructions = models.TextField(
        null=False,
        blank=False
    )
    prep_time = models.PositiveIntegerField(
        null=False,
        blank=False,
    )  # in minutes
    cook_time = models.PositiveIntegerField(
        null=False,
        blank=False,
    )
    serving_way = models.CharField(
        max_length=20,
        choices=CHOICES,
        null=False,
        blank=False
    )
    image_url = models.URLField(
        blank=True,
        null=True,
    )
    # author = models.ForeignKey(
    #     settings.AUTH_USER_MODEL,
    #     on_delete=models.CASCADE
    # )

    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True, blank=True)


@receiver(pre_save, sender=Recipe)
def set_recipe_author(sender, instance, **kwargs):
    if not instance.author:
        instance.author = instance._current_user

# TODO create a model for menu, user reviews, contact us