from django.urls import path

from course.apps import CourseConfig
from rest_framework.routers import DefaultRouter

from course.views import CourseViewSet, CourseCreateAPIViewByLessonId

app_name = CourseConfig.name
router = DefaultRouter()
router.register(r'', CourseViewSet, basename='course')

urlpatterns = [
    path('create_by_id/', CourseCreateAPIViewByLessonId.as_view(), name='create_course_by_lesson_id')
] + router.urls
