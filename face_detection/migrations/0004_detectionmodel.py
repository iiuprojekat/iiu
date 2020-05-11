# Generated by Django 3.0.2 on 2020-05-10 20:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('face_detection', '0003_imagemodel_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='DetectionModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_name', models.CharField(blank=True, max_length=255)),
                ('file_type', models.CharField(choices=[('IMAGE', 'IMAGE'), ('VIDEO', 'VIDEO')], max_length=5)),
                ('detected_faces', models.PositiveSmallIntegerField()),
                ('date', models.DateField(auto_now_add=True)),
                ('time', models.TimeField(auto_now_add=True)),
                ('size', models.BigIntegerField()),
            ],
        ),
    ]
