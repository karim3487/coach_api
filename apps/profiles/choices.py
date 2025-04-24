from django.db import models


class Gender(models.TextChoices):
    MALE = "male", "Male"
    FEMALE = "female", "Female"
