# Generated by Django 4.2.4 on 2023-09-01 17:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0002_course_lesson'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='title',
            field=models.CharField(max_length=150, unique=True, verbose_name='название'),
        ),
    ]
