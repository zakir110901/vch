# Generated by Django 4.1.7 on 2023-03-22 06:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('superset', '0006_university'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='approval_status',
            field=models.CharField(default='unapproved', max_length=20),
        ),
        migrations.AddField(
            model_name='student',
            name='registration_status',
            field=models.CharField(default='unregistered', max_length=20),
        ),
    ]
