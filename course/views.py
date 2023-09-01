from django.shortcuts import render
from rest_framework import viewsets, generics

from course.models import Course
from course.serializers import CourseSerializer, CourseSerializerByLessonId


# Create your views here.
class CourseViewSet(viewsets.ModelViewSet):
    """Для создание / редактирования / обновления / удаления объектов модели Course."""

    serializer_class = CourseSerializer
    queryset = Course.objects.all()


class CourseCreateAPIViewByLessonId(generics.CreateAPIView):
    """Generic для создания объекта модели Course с добавлением связанного поля lesson по id."""

    serializer_class = CourseSerializerByLessonId

