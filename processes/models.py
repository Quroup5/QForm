from django.db import models


class Process(models.Model):
    PROCESS_TYPE_CHOICES = (
        ("Linear", "linear"),
        ("Free", "free"),
    )
    type = models.CharField(max_length=20, choices=PROCESS_TYPE_CHOICES)  # TODO: Check the max_lenght
    title = models.CharField(max_length=255)
    is_private = models.BooleanField(default=False)
    visitor_count = models.IntegerField(default=0)
    response_count = models.IntegerField(default=0)
    password = models.CharField(max_length=255, null=True)


class FormProcess(models.Model):
    order = models.JSONField(default=list)

    process = models.ForeignKey('Process', on_delete=models.PROTECT)
    form = models.ForeignKey('forms.Form', on_delete=models.PROTECT)


class Category(models.Model):
    title = models.CharField(max_length=255)

    processes = models.ManyToManyField('Process')
    forms = models.ManyToManyField('forms.Form')
