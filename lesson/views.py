from django.shortcuts import render
from rest_framework import generics

from lesson.models import Lesson
from lesson.serializers import LessonSerializer


# Create your views here.
class LessonCreateAPIView(generics.CreateAPIView):
    """Для создание объектов модели Lesson."""
    serializer_class = LessonSerializer


class LessonListAPIView(generics.ListAPIView):
    """Для просмотра всех объектов модели Lesson."""
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    """Для детализации информации конкретного объекта модели Lesson."""
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonUpdateAPIView(generics.UpdateAPIView):
    """Для изменения объектов модели Lesson."""
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonDeleteAPIView(generics.DestroyAPIView):
    """Для удаления объектов модели Lesson."""
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
