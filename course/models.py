from django.db import models

from users.models import NULLABLE


# Create your models here.
class Course(models.Model):
    title = models.CharField(max_length=150, verbose_name='название')
    picture = models.ImageField(upload_to='courses/', verbose_name='превью', **NULLABLE)
    description = models.TextField(max_length=1000, verbose_name='описание')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'
        ordering = ('-title', )
