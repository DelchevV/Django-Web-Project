from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth import models as auth_models, get_user_model
from django.conf import settings
from django.db.models.signals import pre_save
from django.dispatch import receiver


def is_old_enough(value):
    if value < 12:
        raise ValidationError('You have to be at least 12 years old to use this app!')


def is_only_letters(value):
    for ch in value:
        if not ch.isalpha() and not ch == ' ':
            raise ValidationError('Title must contains only letters!')


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

    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True, blank=True)


@receiver(pre_save, sender=Recipe)
def set_recipe_author(sender, instance, **kwargs):
    if not instance.author:
        instance.author = instance._current_user


class Feedback(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True, blank=True)
    subject = models.CharField(max_length=100)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


@receiver(pre_save, sender=Feedback)
def set_feedback_author(sender, instance, **kwargs):
    if not instance.user:
        instance.user = instance._current_user


class CookedFood(models.Model):
    CHOICES = (
        ('Breakfast', 'Breakfast'),
        ('Lunch', 'Lunch'),
        ('Snack', 'Snack'),
        ('Dinner', 'Dinner'),
    )
    food_img=models.URLField(
        null=False,
        blank=False,
        default='https://images.unsplash.com/photo-1604135307399-86c6ce0aba8e?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=1374&q=80'
    )
    food_type = models.CharField(
        choices=CHOICES,
        max_length=10,
        null=False,
        blank=False
    )
    food_name = models.CharField(
        max_length=50,
        null=False,
        blank=False,
        validators=[is_only_letters]
    )
    description = models.TextField(
        null=False,
        blank=False
    )
    price = models.DecimalField(
        blank=False,
        null=False,
        max_digits=10,
        decimal_places=2
    )


class Chef(models.Model):
    CHOICES = (
        ('Pastry chef', 'Pastry chef'),
        ('Line cook', 'Line cook'),
        ('Chef', 'Chef'),
        ('Sous chef', 'Sous chef'),
        ('Culinary manager', 'Culinary manager'),
        ('Executive chef', 'Executive chef'),
    )
    first_name = models.CharField(
        max_length=100,
        blank=False,
        null=False
    )
    last_name = models.CharField(
        max_length=100,
        blank=False,
        null=False
    )

    bio = models.TextField()
    profile_picture = models.URLField(
        blank=False,
        null=False
    )
    date_of_birth = models.DateField(
        blank=False,
        null=False
    )
    nationality = models.CharField(
        max_length=50,
        blank=False,
        null=False
    )
    chef_degree = models.CharField(
        choices=CHOICES,
        max_length=50,
        blank=False,
        null=False
    )
    cooked_dishes = models.PositiveIntegerField(
        blank=False,
        null=False
    )


class EBook(models.Model):
    title = models.CharField(max_length=150, blank=False, null=False, validators=[is_only_letters])
    description = models.TextField(blank=False, null=False)
    cover_image = models.URLField(blank=True, null=True)
    chef = models.ForeignKey(Chef, on_delete=models.CASCADE, blank=False, null=False)
    total_dishes = models.PositiveIntegerField(default=0, blank=False, null=False)
    total_breakfast_dishes = models.PositiveIntegerField(default=0, blank=False, null=False)
    total_lunch_dishes = models.PositiveIntegerField(default=0, blank=False, null=False)
    total_dinner_dishes = models.PositiveIntegerField(default=0, blank=False, null=False)

    def __str__(self):
        return self.title
