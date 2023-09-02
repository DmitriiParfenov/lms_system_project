from django.core.management import BaseCommand
from django.db import connection

from course.models import Course
from lesson.models import Lesson
from payments.models import Payment
from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        cur = connection.cursor()
        cur.execute("TRUNCATE TABLE payments_payment RESTART IDENTITY")
        cur.close()

        user_admin = User.objects.get(pk=1) if User.objects.filter(pk=1).exists() else None

        if not user_admin:
            raise Exception('Необходимо создать суперпользователя командой "python manage.py csu"')

        for lesson in Lesson.objects.all():
            payment_create = Payment.objects.create(
                amount=93000,
                payment_method='Наличные',
                is_course_paid=None,
                is_lesson_paid=lesson,
                user=user_admin
            )

        for course in Course.objects.all():
            payment_create = Payment.objects.create(
                amount=93000,
                payment_method='Наличные',
                is_course_paid=course,
                is_lesson_paid=None,
                user=user_admin
            )
