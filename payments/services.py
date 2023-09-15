import os

from django_filters import rest_framework
import stripe
from rest_framework import serializers

from payments.models import Payment

PAYMENT_METHOD_CHOICES = (('Наличные', 'Наличные'), ('Перевод', 'Перевод'),)


class PaymentFilter(rest_framework.FilterSet):
    """Класс для фильтрации полей модели Payment:
    1) payment_method — выбор способа оплаты, наличные или перевод.
    2) lesson — исключает из общей выборки те записи, у которых не оплачен урок.
    3) course — исключает из общей выборки те записи, у которых не оплачен курс."""

    payment_method = rest_framework.TypedChoiceFilter(choices=PAYMENT_METHOD_CHOICES)
    lesson = rest_framework.BooleanFilter(lookup_expr='isnull', exclude=True)
    course = rest_framework.BooleanFilter(lookup_expr='isnull', exclude=True)

    class Meta:
        model = Payment
        fields = ('payment_method', 'lesson', 'course')


def get_session(instance):
    """
    Метод возвращает сессию для оплаты курса и / или урока по API.
    """
    stripe.api_key = os.getenv('STRIPE_API_KEY')

    title_product = f'{instance.lesson}' if instance.lesson else ''
    title_product += f'{instance.course}' if instance.course else ''

    product = stripe.Product.create(name=f"{title_product}")
    price = stripe.Price.create(
        unit_amount=instance.amount,
        currency="rub",
        product=f"{product.id}",
    )

    session = stripe.checkout.Session.create(
        success_url="https://example.com/success",
        line_items=[
            {
                "price": f"{price.id}",
                "quantity": 1,
            },
        ],
        mode="payment",
        customer_email=f"{instance.user.email}"
    )

    return session


def retrieve_session(session):
    """
    Метод возвращает объект сессии по API, id которого был передан в качестве аргумента функции.
    """
    stripe.api_key = os.getenv('STRIPE_API_KEY')

    return stripe.checkout.Session.retrieve(
        session,
    )


