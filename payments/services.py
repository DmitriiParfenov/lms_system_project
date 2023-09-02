from django_filters import rest_framework

from payments.models import Payment

PAYMENT_METHOD_CHOICES = (('Наличные', 'Наличные'), ('Перевод', 'Перевод'),)


class PaymentFilter(rest_framework.FilterSet):
    """Класс для фильтрации полей модели Payment:
    1) payment_method — выбор способа оплаты, наличные или перевод;
    2) is_lesson_paid — исключает из общей выборки те записи, к оторых не оплачен урок;
    3) is_course_paid — исключает из общей выборки те записи, к оторых не оплачен курс."""

    payment_method = rest_framework.TypedChoiceFilter(choices=PAYMENT_METHOD_CHOICES)
    is_lesson_paid = rest_framework.BooleanFilter(lookup_expr='isnull', exclude=True)
    is_course_paid = rest_framework.BooleanFilter(lookup_expr='isnull', exclude=True)

    class Meta:
        model = Payment
        fields = ('payment_method', 'is_lesson_paid', 'is_course_paid')
