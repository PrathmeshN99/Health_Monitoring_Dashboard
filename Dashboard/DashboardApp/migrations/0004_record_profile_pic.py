# Generated by Django 4.0.4 on 2022-06-15 06:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DashboardApp', '0003_rename_records_record'),
    ]

    operations = [
        migrations.AddField(
            model_name='record',
            name='profile_pic',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
