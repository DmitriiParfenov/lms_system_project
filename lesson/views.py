from django.shortcuts import render
from rest_framework import generics
from rest_framework.generics import get_object_or_404

from course.pagination import Pagination
from lesson.models import Lesson
from lesson.permissions import IsOwnerOrIsAuthenticatedOrModerator
from lesson.serializers import LessonSerializer, LessonListSerializer


# Create your views here.
class LessonCreateAPIView(generics.CreateAPIView):
    """Для создания объектов модели Lesson."""

    serializer_class = LessonSerializer
    permission_classes = (IsOwnerOrIsAuthenticatedOrModerator,)

    def perform_create(self, serializer):
        new_mat = serializer.save()
        new_mat.user_lesson = self.request.user
        new_mat.save()


class LessonListAPIView(generics.ListAPIView):
    """Для просмотра всех объектов модели Lesson."""

    serializer_class = LessonListSerializer
    permission_classes = (IsOwnerOrIsAuthenticatedOrModerator,)
    pagination_class = Pagination

    def get_queryset(self):
        """
        Если у текущего пользователя есть расширенные права, то метод возвращает все объекты модели Course, иначе —
        объекты, отфильтрованные по текущему пользователю.
        """
        if self.request.user.has_perm('lesson.view_lesson'):
            return Lesson.objects.all()
        return Lesson.objects.filter(user_lesson=self.request.user)


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    """Для детализации информации конкретного объекта модели Lesson."""

    serializer_class = LessonListSerializer
    queryset = Lesson.objects.all()
    permission_classes = (IsOwnerOrIsAuthenticatedOrModerator,)

    def get_object(self):
        """
        Метод получает объект по "pk", переданному от пользователя. Если такого нет, то возникнет 404 ошибка, иначе —
        метод вернет этот объект, предварительно проверив его права доступа.
        """
        obj = get_object_or_404(self.get_queryset(), pk=self.kwargs["pk"])
        self.check_object_permissions(self.request, obj)
        return obj


class LessonUpdateAPIView(generics.UpdateAPIView):
    """Для изменения объектов модели Lesson."""

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = (IsOwnerOrIsAuthenticatedOrModerator,)

    def get_object(self):
        """
        Метод получает объект по "pk", переданному от пользователя. Если такого нет, то возникнет 404 ошибка, иначе —
        метод вернет этот объект, предварительно проверив его права доступа.
        """
        obj = get_object_or_404(self.get_queryset(), pk=self.kwargs["pk"])
        self.check_object_permissions(self.request, obj)
        return obj


class LessonDeleteAPIView(generics.DestroyAPIView):
    """Для удаления объектов модели Lesson."""

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = (IsOwnerOrIsAuthenticatedOrModerator,)

    def get_object(self):
        """
        Метод получает объект по "pk", переданному от пользователя. Если такого нет, то возникнет 404 ошибка, иначе —
        метод вернет этот объект, предварительно проверив его права доступа.
        """
        obj = get_object_or_404(self.get_queryset(), pk=self.kwargs["pk"])
        self.check_object_permissions(self.request, obj)
        return obj
