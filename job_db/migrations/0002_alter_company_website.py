# Generated by Django 5.1.4 on 2024-12-18 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job_db', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='website',
            field=models.URLField(blank=True, max_length=255, null=True, verbose_name='website'),
        ),
    ]
