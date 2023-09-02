from django.db import models

from users.models import NULLABLE


# Create your models here.
class Payment(models.Model):

    class Kinds(models.TextChoices):
        CASH = ('Наличные', 'Наличные')
        CARD = ('Перевод', 'Перевод')

    user = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name='пользователь')
    date_payment = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='дата_платежа')
    amount = models.FloatField(verbose_name='сумма_оплаты')
    is_lesson_paid = models.ForeignKey('lesson.Lesson', on_delete=models.CASCADE,
                                       verbose_name='урок_оплачен', **NULLABLE)
    is_course_paid = models.ForeignKey('course.Course', on_delete=models.CASCADE,
                                       verbose_name='курс_оплачен', **NULLABLE)
    payment_method = models.CharField(max_length=8, choices=Kinds.choices,
                                      default=Kinds.CARD, verbose_name='способ_оплаты')

    def __str__(self):
        return f'Оплата пользователя — {self.user}'

    class Meta:
        verbose_name = 'оплата'
        verbose_name_plural = 'оплата'
        ordering = ('-amount', )