# Generated by Django 3.2 on 2021-07-16 17:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='room_id',
            field=models.AutoField(max_length=50, primary_key=True, serialize=False),
        ),
    ]
