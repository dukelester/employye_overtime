# Generated by Django 4.0.3 on 2022-04-19 11:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('overtime', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='overtime',
            name='my_employee',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='overtime.employee'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='requestedovertimes',
            name='employoer',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='employer', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
