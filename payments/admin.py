from django.contrib import admin

from payments.models import Payment


# Register your models here.
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'amount', 'is_lesson_paid', 'is_course_paid', 'payment_method', 'user')
    list_display_links = ('amount', 'is_lesson_paid', 'is_course_paid', 'payment_method')
    search_fields = ('amount', 'is_lesson_paid', 'is_course_paid', 'payment_method')
