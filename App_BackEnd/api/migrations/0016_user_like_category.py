# Generated by Django 3.2 on 2021-07-20 16:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0015_user_last_login'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='like_category',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
