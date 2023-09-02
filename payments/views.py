from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import OrderingFilter

from payments.models import Payment
from payments.serializers import PaymentSerializer
from payments.services import PaymentFilter


# Create your views here.
class PaymentListAPIView(generics.ListAPIView):
    """Для создание / редактирования / обновления / удаления объектов модели Payment. Доступна сортировка по
    полю <date_payment> и добавлена фильтрация по полям <payment_method>, <is_lesson_paid>, <is_course_paid>."""

    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = (OrderingFilter, DjangoFilterBackend)
    ordering_fields = ('date_payment',)
    filterset_class = PaymentFilter

