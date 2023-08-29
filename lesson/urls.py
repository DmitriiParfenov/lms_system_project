from django.urls import path

from lesson.apps import LessonConfig
from lesson.views import LessonListAPIView, LessonRetrieveAPIView, LessonCreateAPIView, LessonUpdateAPIView, \
    LessonDeleteAPIView

app_name = LessonConfig.name

urlpatterns = [
    path('', LessonListAPIView.as_view(), name='lesson_list'),
    path('<int:pk>/', LessonRetrieveAPIView.as_view(), name='lesson_detail'),
    path('create_lesson/', LessonCreateAPIView.as_view(), name='lesson_create'),
    path('update/<int:pk>/', LessonUpdateAPIView.as_view(), name='lesson_delete'),
    path('delete/<int:pk>/', LessonDeleteAPIView.as_view(), name='lesson_delete')
]