# Generated by Django 3.2.7 on 2021-10-07 18:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('spodaily_api', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='activity',
            old_name='exercise_id',
            new_name='exercise',
        ),
        migrations.RenameField(
            model_name='activity',
            old_name='session_id',
            new_name='session',
        ),
    ]