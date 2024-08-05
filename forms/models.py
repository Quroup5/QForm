from django.db import models
from django.contrib.auth.hashers import make_password, check_password


class Category(models.Model):
    title = models.CharField(max_length=255)
    user = models.ForeignKey('users.User', on_delete=models.PROTECT)


class Form(models.Model):
    title = models.CharField(max_length=100)
    visitor_count = models.IntegerField(default=0)
    response_count = models.IntegerField(default=0)
    is_private = models.BooleanField(default=False)
    password = models.CharField(max_length=50, null=True)

    user = models.ForeignKey('users.User', on_delete=models.PROTECT)
    category = models.ForeignKey('Category', on_delete=models.PROTECT, null=True)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def save(self, *args, **kwargs):
        if not self.password.startswith('pbkdf2_sha256$'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)


class Question(models.Model):
    SELECT = "select"
    CHECKBOX = "checkbox"
    TEXT = "text"

    QUESTION_TYPE_CHOICES = (
        (SELECT, "select"),
        (CHECKBOX, "checkbox"),
        (TEXT, "text"),
    )
    name = models.CharField(max_length=50)
    label = models.CharField(max_length=255)
    required = models.BooleanField(default=False)
    type = models.CharField(max_length=20, choices=QUESTION_TYPE_CHOICES)
    metadata = models.JSONField()

    form = models.ForeignKey('Form', on_delete=models.PROTECT)

    class Meta:
        unique_together = ('name', 'form',)


class Process(models.Model):
    LINEAR = "linear"
    FREE = "free"

    PROCESS_TYPE_CHOICES = (
        (LINEAR, "linear"),
        (FREE, "free"),
    )
    type = models.CharField(max_length=10, choices=PROCESS_TYPE_CHOICES)
    name = models.CharField(max_length=50)
    title = models.CharField(max_length=255)
    is_private = models.BooleanField(default=False)
    visitor_count = models.IntegerField(default=0)
    response_count = models.IntegerField(default=0)
    password = models.CharField(max_length=50, null=True)

    category = models.ForeignKey('Category', on_delete=models.PROTECT, null=True)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def save(self, *args, **kwargs):
        # Ensure the password is hashed before saving
        if not self.password.startswith('pbkdf2_sha256$'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)


class FormProcess(models.Model):
    order = models.PositiveSmallIntegerField()

    process = models.ForeignKey('Process', on_delete=models.PROTECT)
    form = models.ForeignKey('Form', on_delete=models.PROTECT)

    class Meta:
        unique_together = ('order', 'process', 'form',)


class Response(models.Model):
    answer = models.JSONField()

    form = models.ForeignKey('Form', on_delete=models.PROTECT)
    user = models.ForeignKey('users.User', on_delete=models.PROTECT, null=True)
