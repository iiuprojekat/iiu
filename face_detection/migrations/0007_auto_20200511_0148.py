# Generated by Django 3.0.2 on 2020-05-10 23:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('face_detection', '0006_auto_20200511_0027'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detectionmodel',
            name='date',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='detectionmodel',
            name='time',
            field=models.CharField(max_length=255),
        ),
    ]
