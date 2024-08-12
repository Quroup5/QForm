from django.db import models
from django.contrib.auth.hashers import make_password


class Category(models.Model):
    title = models.CharField(max_length=255)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Form(models.Model):
    title = models.CharField(max_length=100)
    visitor_count = models.IntegerField(default=0)
    answer_count = models.IntegerField(default=0)
    is_private = models.BooleanField(default=False)
    password = models.CharField(max_length=50, null=True)

    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.password and not self.password.startswith('pbkdf2_'):
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

    form = models.ForeignKey('Form', on_delete=models.CASCADE)

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
    visitor_count = models.IntegerField(default=0)
    answer_count = models.IntegerField(default=0)
    is_private = models.BooleanField(default=False)
    password = models.CharField(max_length=50, null=True)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.password and not self.password.startswith('pbkdf2_'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)


class FormProcess(models.Model):
    process = models.ForeignKey('Process', on_delete=models.CASCADE)
    form = models.ForeignKey('Form', on_delete=models.CASCADE)
    order = models.PositiveSmallIntegerField(null=True, blank=True)

    class Meta:
        unique_together = ('process', 'order')


class Answer(models.Model):
    answer = models.JSONField()
    process = models.ForeignKey('Process', on_delete=models.CASCADE, null=True, blank=True)
    form = models.ForeignKey('Form', on_delete=models.CASCADE)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, null=True, blank=True)
    responder_nickname = models.CharField(max_length=255)

    # class Meta:
    #     unique_together = ('form', 'process', 'responder_nickname')