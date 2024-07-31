from django.db import models


class Form(models.Model):
    title = models.CharField(max_length=100)
    visitor_count = models.IntegerField(default=0)
    response_count = models.IntegerField(default=0)
    is_private = models.BooleanField(default=False)
    password = models.CharField(max_length=100, null=True)

    user = models.ForeignKey('users.User', on_delete=models.CASCADE)


# class PrivateForm(Form):
#     is_private = models.BooleanField(default=False)
#     password = models.CharField(max_length=100, null=True)


class Question(models.Model):
    QUESTION_TYPE_CHOICES = (
        ("Select", "select"),
        ("Checkbox", "checkbox"),
        ("Text", "text"),
    )
    type = models.CharField(max_length=20, choices=QUESTION_TYPE_CHOICES)
    description = models.JSONField(max_length=1000)  # TODO: Make the max_length better

    form = models.ForeignKey('Form', on_delete=models.PROTECT)


class Response(models.Model):
    answer = models.JSONField(max_length=1000)      # TODO: Make the max_length better

    form = models.ForeignKey('Form', on_delete=models.PROTECT)
    user = models.ForeignKey('users.User', on_delete=models.PROTECT)
