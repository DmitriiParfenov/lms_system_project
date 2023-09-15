from rest_framework import serializers

from course.models import Course
from course.serializers import CourseSerializer
from lesson.models import Lesson
from lesson.serializers import LessonSerializer
from payments.models import Payment
from payments.services import retrieve_session
from users.models import User
from users.serializers import UserSerializerForPayment


class PaymentRetrieveSerializer(serializers.ModelSerializer):
    user = UserSerializerForPayment(read_only=True)
    lesson = LessonSerializer(read_only=True)
    course = CourseSerializer(read_only=True)
    url_for_pay = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Payment
        fields = ('user', 'date_payment', 'amount', 'lesson', 'course', 'payment_method', 'is_paid', 'url_for_pay')

    def get_url_for_pay(self, instance) -> None | str | dict:
        """Метод возвращает ссылку на оплату объекта. Если объект оплачен или срок действия сессии истек, то метод
        вернет None."""

        if instance.is_paid:
            return None

        session = retrieve_session(instance.session)
        if session.payment_status == 'unpaid' and session.status == 'open':
            return session.url
        elif session.payment_status == 'paid' and session.status == 'complete':
            return None
        status = {
            'session': 'Срок действия сессии истек. Создайте платеж заново.'
        }
        return status


class PaymentCreateSerializer(serializers.ModelSerializer):
    lesson = serializers.SlugRelatedField(slug_field='title', queryset=Lesson.objects.all(),
                                          allow_null=True, required=False)
    course = serializers.SlugRelatedField(slug_field='title', queryset=Course.objects.all(),
                                          allow_null=True, required=False)
    user = serializers.SlugRelatedField(slug_field='email', queryset=User.objects.all())

    class Meta:
        model = Payment
        fields = ('amount', 'lesson', 'course', 'payment_method', 'user', 'session')


class PaymentListSerializer(serializers.ModelSerializer):
    user = UserSerializerForPayment(read_only=True)
    lesson = LessonSerializer(read_only=True)
    course = CourseSerializer(read_only=True)

    class Meta:
        model = Payment
        fields = ('user', 'date_payment', 'amount', 'lesson', 'course', 'payment_method', 'is_paid',)
