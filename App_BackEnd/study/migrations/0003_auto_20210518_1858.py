# Generated by Django 3.2 on 2021-05-18 18:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('study', '0002_auto_20210518_1414'),
    ]

    operations = [
        migrations.AlterField(
            model_name='daily_1m_content',
            name='concentrate',
            field=models.CharField(max_length=2, null=True),
        ),
        migrations.AlterField(
            model_name='daily_1m_content',
            name='datetime',
            field=models.CharField(max_length=20, null=True),
        ),
    ]