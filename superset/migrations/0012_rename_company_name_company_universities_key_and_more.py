# Generated by Django 4.1.7 on 2023-04-10 08:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('superset', '0011_alter_company_company_name_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='company_universities',
            old_name='Company_name',
            new_name='key',
        ),
        migrations.AddField(
            model_name='company_universities',
            name='company_name',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]
