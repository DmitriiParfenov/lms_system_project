from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, serializers
from rest_framework.filters import OrderingFilter
from rest_framework.generics import get_object_or_404

from payments.models import Payment
from payments.permissions import IsOwner
from payments.serializers import PaymentCreateSerializer, PaymentRetrieveSerializer, PaymentListSerializer
from payments.services import PaymentFilter, get_session, retrieve_session


# Create your views here.
class PaymentListAPIView(generics.ListAPIView):
    """Для просмотра объектов модели Payment. Доступна сортировка по полю <date_payment> и добавлена фильтрация
    по полям <payment_method>, <is_lesson_paid>, <is_course_paid>."""

    serializer_class = PaymentListSerializer
    filter_backends = (OrderingFilter, DjangoFilterBackend)
    ordering_fields = ('date_payment',)
    filterset_class = PaymentFilter
    permission_classes = (IsOwner,)

    def get_queryset(self):
        return Payment.objects.filter(user=self.request.user)


class PaymentRetrieveAPIView(generics.RetrieveAPIView):
    """Для просмотра детализированной информации текущего объекта модели Payment."""

    serializer_class = PaymentRetrieveSerializer
    permission_classes = (IsOwner,)
    queryset = Payment.objects.all()

    def get_object(self):
        """
        Метод получает объект по "pk", переданному от пользователя. Если такого нет, то возникнет 404 ошибка, иначе —
        метод вернет этот объект, предварительно проверив его права доступа.
        """
        obj = get_object_or_404(self.get_queryset(), pk=self.kwargs["pk"])
        session = retrieve_session(obj.session)
        if session.payment_status == 'paid' and session.status == 'complete':
            obj.is_paid = True
            obj.save()
        self.check_object_permissions(self.request, obj)
        return obj


class PaymentCreateAPIView(generics.CreateAPIView):
    """Для создания нового объекта модели Payment."""

    serializer_class = PaymentCreateSerializer
    permission_classes = (IsOwner,)
    queryset = Payment.objects.all()

    def perform_create(self, serializer):
        lesson = serializer.validated_data.get('lesson')
        course = serializer.validated_data.get('course')
        if not lesson and not course:
            raise serializers.ValidationError({
                'non_empty_fields': 'Заполните хотя бы один из двух полей: lesson или course'
            })
        new_mat = serializer.save()
        new_mat.user = self.request.user
        new_mat.session = get_session(new_mat).id
        new_mat.save()
