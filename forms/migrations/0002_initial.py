# Generated by Django 4.2 on 2024-08-11 12:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('forms', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='response',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='question',
            name='form',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='forms.form'),
        ),
        migrations.AddField(
            model_name='process',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='forms.category'),
        ),
        migrations.AddField(
            model_name='formprocess',
            name='form',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='forms.form'),
        ),
        migrations.AddField(
            model_name='formprocess',
            name='process',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='forms.process'),
        ),
        migrations.AddField(
            model_name='form',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='forms.category'),
        ),
        migrations.AddField(
            model_name='form',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='category',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='question',
            unique_together={('name', 'form')},
        ),
        migrations.AlterUniqueTogether(
            name='formprocess',
            unique_together={('order', 'process', 'form')},
        ),
    ]
