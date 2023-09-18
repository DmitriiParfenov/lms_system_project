from celery import shared_task
from django.core.mail import send_mail

from config import settings
from course.models import Course


@shared_task
def send_email_updated_course(pk_course):
    """
    Метод для отправки сообщения подписчикам после обновления материалов курса при условии, если курс не обновлялся
    более 4 часов.
    """
    course = Course.objects.filter(pk=pk_course).first()
    if course.exists():
        delta = course.changed - course.published
        if delta.total_seconds() >= 14400:
            for data in course.material.all():
                send_mail(
                    subject='Обновление материалов курса',
                    message=f'Здравствуйте, {data.user.email}!\n\nОбновился материал по курсу {data.course.title}!\n\n'
                            f'Подробнее: http://127.0.0.1:8000/courses/{pk_course}/\n\n\n'
                            f'С уважением, администрация сайта!',
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[data.user.email],
                    fail_silently=False
                )
    print(f'Похоже, что курса с идентификатором "{pk_course}" не существует.')
