# Generated by Django 4.0.3 on 2022-04-19 11:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('overtime', '0002_overtime_my_employee_requestedovertimes_employoer'),
    ]

    operations = [
        migrations.RenameField(
            model_name='requestedovertimes',
            old_name='employoer',
            new_name='employer',
        ),
    ]
