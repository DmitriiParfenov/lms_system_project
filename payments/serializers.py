from rest_framework import serializers

from course.serializers import CourseSerializer
from lesson.serializers import LessonSerializer
from payments.models import Payment
from users.serializers import UserSerializerForPayment


class PaymentSerializer(serializers.ModelSerializer):
    user = UserSerializerForPayment(read_only=True)
    is_lesson_paid = LessonSerializer(read_only=True)
    is_course_paid = CourseSerializer(read_only=True)

    class Meta:
        model = Payment
        fields = ('user', 'date_payment', 'amount', 'is_lesson_paid', 'is_course_paid', 'payment_method',)
