# Generated by Django 5.1 on 2024-09-15 13:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gymmy', '0011_workoutprogress_exercise'),
    ]

    operations = [
        migrations.AddField(
            model_name='routines',
            name='popularity_count',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
