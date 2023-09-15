# Generated by Django 4.2.4 on 2023-09-14 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='payment',
            old_name='is_course_paid',
            new_name='course',
        ),
        migrations.RenameField(
            model_name='payment',
            old_name='is_lesson_paid',
            new_name='lesson',
        ),
        migrations.AddField(
            model_name='payment',
            name='is_paid',
            field=models.BooleanField(default=False, verbose_name='статус_оплаты'),
        ),
    ]