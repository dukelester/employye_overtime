# Generated by Django 4.0.3 on 2022-04-02 11:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('overtime', '0009_employee_is_email_verified'),
    ]

    operations = [
        migrations.CreateModel(
            name='Overtime',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('overtime_date', models.DateField()),
                ('overtime_hours', models.IntegerField()),
                ('description', models.TextField()),
                ('overtime_type', models.CharField(max_length=200)),
                ('overtime_pay', models.DecimalField(decimal_places=0, max_digits=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('approved_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('my_employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='overtime.employee')),
            ],
            options={
                'verbose_name': 'Over Time',
                'verbose_name_plural': 'Over Time',
            },
        ),
    ]
