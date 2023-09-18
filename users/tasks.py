from datetime import datetime, timezone

from celery import shared_task
from django.db.models import F
from django.db.models.functions import ExtractDay
from django_celery_beat.models import PeriodicTask, CrontabSchedule

from users.models import User


@shared_task
def inactivate_user():
    """Метод инактивирует пользователей, которые не были авторизованы на сайте более 30 дней."""

    now = datetime.now(timezone.utc)
    users = User.objects.annotate(delta=(ExtractDay(now - F('last_login')))).filter(delta__gte=30)
    if users:
        for user in users:
            if not user.is_superuser:
                user.is_active = False
                user.save(update_fields=['is_active'])


schedule, _ = CrontabSchedule.objects.get_or_create(
    minute='*',
    hour='15',
    day_of_week='*',
    day_of_month='*',
    month_of_year='*',
)

PeriodicTask.objects.get_or_create(
    crontab=schedule,
    name='Inactivate users',
    task='users.tasks.inactivate_user',
)
