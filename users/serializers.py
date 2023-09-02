from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    payments = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'phone', 'city', 'payments')

    def get_payments(self, instance):
        return instance.payment_set.all().select_related('is_course_paid', 'is_lesson_paid').values(
            'date_payment',
            'amount',
            'payment_method',
            'is_course_paid__title',
            'is_lesson_paid__title'
        )


class UserSerializerForPayment(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'phone', 'city')
