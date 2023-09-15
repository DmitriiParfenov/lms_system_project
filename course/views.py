from rest_framework import viewsets, generics, serializers

from course.models import Course, Subscription
from course.pagination import Pagination
from course.permissions import IsOwnerOrModerator, IsOwnerSubscription
from course.serializers import CourseSerializer, CourseSerializerByLessonId, SubscriptionSerializer, \
    SubscriptionUnsubscribeSerializer


# Create your views here.
class CourseViewSet(viewsets.ModelViewSet):
    """Для создание / редактирования / обновления / удаления объектов модели Course."""

    serializer_class = CourseSerializer
    permission_classes = (IsOwnerOrModerator,)
    pagination_class = Pagination

    def get_queryset(self):
        """
        Если у текущего пользователя есть расширенные права, то метод возвращает все объекты модели Course, иначе —
        объекты, отфильтрованные по текущему пользователю.
        """
        if self.request.user.has_perms(['course.view_course']):
            return Course.objects.all()
        return Course.objects.filter(user_course=self.request.user.id)

    def perform_create(self, serializer):
        new_obj = serializer.save()
        for lesson in new_obj.lesson.all():
            if not lesson.user_lesson:
                lesson.user_lesson = self.request.user
                lesson.save()
        new_obj.user_course = self.request.user
        new_obj.save()

    def perform_update(self, serializer):
        updated_obj = serializer.save()
        if not self.request.user.is_staff:
            updated_obj.user_course = self.request.user
        updated_obj.save()


class CourseCreateAPIViewByLessonId(generics.CreateAPIView):
    """Generic для создания объекта модели Course с добавлением связанного поля lesson по id."""

    serializer_class = CourseSerializerByLessonId
    permission_classes = (IsOwnerOrModerator,)

    def perform_create(self, serializer):
        owner = serializer.save()
        for lesson in owner.lesson.all():
            if not lesson.user_lesson:
                lesson.user_lesson = self.request.user
                lesson.save()
        owner.user_course = self.request.user
        owner.save()


class SubscriptionCreateAPIView(generics.CreateAPIView):
    """Для создания подписки на указанный курс для текущего авторизованного пользователя."""
    serializer_class = SubscriptionSerializer
    permission_classes = (IsOwnerSubscription,)

    def perform_create(self, serializer):
        errors = {}
        for _ in serializer.validated_data:
            course_title = serializer.validated_data.get('course')
            user_subscriptions = self.request.user.subscriber.filter(course=course_title.pk)
            if user_subscriptions:
                errors['user'] = 'Текущий пользователь уже подписан на данный курс'
        if errors:
            raise serializers.ValidationError(errors)
        new_mat = serializer.save()
        new_mat.user = self.request.user
        new_mat.save()


class UnsubscribeAPIView(generics.UpdateAPIView):
    """Для отписки от указанного курса для текущего авторизованного пользователя."""

    serializer_class = SubscriptionUnsubscribeSerializer
    permission_classes = (IsOwnerSubscription,)

    def get_queryset(self):
        return Subscription.objects.filter(user=self.request.user.pk)

    def perform_update(self, serializer):
        new_mat = serializer.save()
        new_mat.user = None
        new_mat.save()
