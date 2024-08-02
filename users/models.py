from django.contrib.auth import models
from django.db.models import CharField


class User(models.AbstractUser):
    national_id = CharField(max_length=10)  # TODO: Change this to make it more safe. Take a look at https://docs.allauth.org/en/latest/
    cellphone_number = CharField(max_length=11)

