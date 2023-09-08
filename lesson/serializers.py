from rest_framework import serializers

from lesson.models import Lesson
from users.models import User


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ('id', 'title', 'description', 'url_video')


class LessonListSerializer(serializers.ModelSerializer):
    user_lesson = serializers.SlugRelatedField(slug_field='email', queryset=User.objects.all())

    class Meta:
        model = Lesson
        fields = ('id', 'title', 'description', 'url_video', 'user_lesson')
