from django.contrib import admin

from payments.models import Payment


# Register your models here.
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('amount', 'is_lesson_paid', 'is_course_paid', 'payment_method')
    list_display_links = ('amount', 'is_lesson_paid', 'is_course_paid', 'payment_method')
    search_fields = ('amount', 'is_lesson_paid', 'is_course_paid', 'payment_method')
