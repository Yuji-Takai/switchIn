# Generated by Django 2.0.6 on 2018-07-10 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('switchinweb', '0004_policy_vehicle'),
    ]

    operations = [
        migrations.AddField(
            model_name='policy',
            name='city',
            field=models.CharField(default='general', max_length=40),
        ),
    ]
