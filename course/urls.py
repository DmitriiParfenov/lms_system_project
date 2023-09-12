from django.urls import path

from course.apps import CourseConfig
from rest_framework.routers import DefaultRouter

from course.views import CourseViewSet, CourseCreateAPIViewByLessonId, SubscriptionCreateAPIView, UnsubscribeAPIView

app_name = CourseConfig.name
router = DefaultRouter()
router.register(r'', CourseViewSet, basename='course')

urlpatterns = [
    path('create_by_id/', CourseCreateAPIViewByLessonId.as_view(), name='create_course_by_lesson_id'),
    path('create_subscription/', SubscriptionCreateAPIView.as_view(), name='subscription_create'),
    path('unsubscribe/<int:pk>/', UnsubscribeAPIView.as_view(), name='unsubscribe')
] + router.urls
