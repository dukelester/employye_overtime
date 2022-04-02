# Generated by Django 4.0.3 on 2022-04-02 12:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('overtime', '0010_overtime'),
    ]

    operations = [
        migrations.AddField(
            model_name='overtime',
            name='total',
            field=models.DecimalField(decimal_places=0, default=2000, max_digits=10),
            preserve_default=False,
        ),
    ]