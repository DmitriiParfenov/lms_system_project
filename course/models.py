from django.db import models

from users.models import NULLABLE


# Create your models here.
class Course(models.Model):
    title = models.CharField(max_length=150, verbose_name='название', unique=True)
    picture = models.ImageField(upload_to='courses/', verbose_name='превью', **NULLABLE)
    description = models.TextField(max_length=1000, verbose_name='описание')
    lesson = models.ManyToManyField('lesson.Lesson', verbose_name='урок_курса')
    user_course = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name='создатель', **NULLABLE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'
        ordering = ('-title',)


class Subscription(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.SET_NULL,
                             verbose_name='пользователь', related_name='subscriber', **NULLABLE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE,
                               verbose_name='курс', related_name='material')

    def __str__(self):
        return f'Подписка {self.course}'

    class Meta:
        verbose_name = 'подписка'
        verbose_name_plural = 'подписки'
