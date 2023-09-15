from django.contrib import admin

from payments.models import Payment


# Register your models here.
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'amount', 'lesson', 'course', 'payment_method', 'user', 'is_paid')
    list_display_links = ('amount', 'lesson', 'course', 'payment_method')
    search_fields = ('amount', 'lesson', 'course', 'payment_method')
