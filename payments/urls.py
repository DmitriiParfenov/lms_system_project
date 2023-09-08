from django.urls import path

from payments.apps import PaymentsConfig
from payments.views import PaymentListAPIView, PaymentRetrieveAPIView, PaymentCreateAPIView

app_name = PaymentsConfig.name

urlpatterns = [
    path('', PaymentListAPIView.as_view(), name='payment_list'),
    path('<int:pk>/', PaymentRetrieveAPIView.as_view(), name='payment_detail'),
    path('create_payments/', PaymentCreateAPIView.as_view(), name='create_payments')
]