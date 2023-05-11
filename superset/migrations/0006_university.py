# Generated by Django 4.1.7 on 2023-03-22 05:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('superset', '0005_alter_uvstudents_file'),
    ]

    operations = [
        migrations.CreateModel(
            name='University',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('College', models.CharField(max_length=250, unique=True)),
                ('University', models.CharField(max_length=250)),
                ('Passphrase', models.CharField(max_length=250, unique=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('Full_Name', models.CharField(max_length=250)),
            ],
        ),
    ]
