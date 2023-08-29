from django.db import models

from users.models import NULLABLE


# Create your models here.
class Lesson(models.Model):
    title = models.CharField(max_length=150, verbose_name='название')
    description = models.TextField(max_length=1000, verbose_name='описание')
    picture = models.ImageField(upload_to='lessons/', verbose_name='превью', **NULLABLE)
    url_video = models.CharField(max_length=250, verbose_name='ссылка')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'
        ordering = ('-title', )