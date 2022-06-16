# Generated by Django 4.0.4 on 2022-06-16 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DashboardApp', '0006_rename_image_profile_profile_pic_remove_record_temp_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='blood_group',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='record',
            name='AQI',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='record',
            name='Body_Temperature',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='record',
            name='Humidity',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='record',
            name='Temperature',
            field=models.FloatField(default=0),
        ),
    ]
