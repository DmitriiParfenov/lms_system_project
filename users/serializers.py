from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    payments = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'phone', 'city', 'payments', 'is_active')
        ref_name = 'UserSerializer'

    def get_payments(self, instance):
        return instance.payment_set.all().select_related('course', 'lesson').values(
            'date_payment',
            'amount',
            'payment_method',
            'course__title',
            'lesson__title'
        )


class UserSerializerForPayment(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'email', 'phone', 'city')
        ref_name = 'UserSerializerForPayment'


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'phone', 'city', 'avatar',)
        ref_name = 'UserUpdateSerializer'
