# Generated by Django 2.0.6 on 2018-07-10 20:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('switchinweb', '0005_policy_city'),
    ]

    operations = [
        migrations.RenameField(
            model_name='state',
            old_name='avg_injury',
            new_name='avg_fatal',
        ),
        migrations.AddField(
            model_name='state',
            name='avg_pain',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='state',
            name='avg_severe',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='state',
            name='avg_visible',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='state',
            name='fatal_num',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='state',
            name='pain_num',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='state',
            name='severe_num',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='state',
            name='total_pop',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='state',
            name='vehicle_pop',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='state',
            name='visible_num',
            field=models.PositiveIntegerField(default=0),
        ),
    ]