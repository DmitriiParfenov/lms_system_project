from rest_framework import serializers

from course.models import Course
from course.serializers import CourseSerializer
from lesson.models import Lesson
from lesson.serializers import LessonSerializer
from payments.models import Payment
from users.models import User
from users.serializers import UserSerializerForPayment


class PaymentSerializer(serializers.ModelSerializer):
    user = UserSerializerForPayment(read_only=True)
    is_lesson_paid = LessonSerializer(read_only=True)
    is_course_paid = CourseSerializer(read_only=True)

    class Meta:
        model = Payment
        fields = ('user', 'date_payment', 'amount', 'is_lesson_paid', 'is_course_paid', 'payment_method',)


class PaymentCreateSerializer(serializers.ModelSerializer):
    is_lesson_paid = serializers.SlugRelatedField(slug_field='title', queryset=Lesson.objects.all(), allow_null=True)
    is_course_paid = serializers.SlugRelatedField(slug_field='title', queryset=Course.objects.all(), allow_null=True)
    user = serializers.SlugRelatedField(slug_field='email', queryset=User.objects.all())

    class Meta:
        model = Payment
        fields = ('amount', 'is_lesson_paid', 'is_course_paid', 'payment_method', 'user')
