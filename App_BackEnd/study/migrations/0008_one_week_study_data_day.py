# Generated by Django 3.2 on 2021-05-27 00:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('study', '0007_auto_20210525_0409'),
    ]

    operations = [
        migrations.AddField(
            model_name='one_week_study_data',
            name='day',
            field=models.DateField(null=True),
        ),
    ]
