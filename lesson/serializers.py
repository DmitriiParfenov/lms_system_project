from rest_framework import serializers

from lesson.models import Lesson
from users.models import User
import re


class LessonSerializer(serializers.ModelSerializer):
    def validate_url_video(self, data):
        errors = {}
        url = re.search(r'(https?://)?(www\d?\.)?(?P<name>[\w-]+)\.', data)
        if not url:
            errors['invalid_url'] = 'Некорректная ссылка на видеоматериал.'
        else:
            url_domain = url.group('name')
            if url_domain.lower() != 'youtube':
                errors['invalid_domain'] = 'Видеоматериалы должны быть размещены на видеохостингe <Youtube>.'
        if errors:
            raise serializers.ValidationError(errors)
        return data

    class Meta:
        model = Lesson
        fields = ('id', 'title', 'description', 'url_video')


class LessonListSerializer(serializers.ModelSerializer):
    user_lesson = serializers.SlugRelatedField(slug_field='email', queryset=User.objects.all())

    class Meta:
        model = Lesson
        fields = ('id', 'title', 'description', 'url_video', 'user_lesson')
