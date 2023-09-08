from rest_framework import serializers

from course.models import Course

from lesson.models import Lesson
from lesson.serializers import LessonSerializer
from users.models import User


class CourseSerializer(serializers.ModelSerializer):
    """Класс сериализут поля модели Course: <title>, <description>. Поле <lesson> сериализуется через вложенный
    сериализатор LessonSerializer с полным описанием полей вложенного сериализатора, при чем, если при создании
    объекта модели Course и при описании всех полей вложенного сериализатора для Lesson не существует объекта
    модели Lesson, то он будет создан. Поле <count_lesson> — это общее количество уроков в курсе."""

    lesson = LessonSerializer(many=True)
    count_lesson = serializers.SerializerMethodField()
    user_course = serializers.SlugRelatedField(slug_field='email', queryset=User.objects.all())

    class Meta:
        model = Course
        fields = ('id', 'title', 'description', 'count_lesson', 'lesson', 'user_course')

    def create(self, validated_data):
        """Метод создает объект модели Course с указанием полей для вложенного объекта модели Lesson. Если текущего
        объекта Lesson нет в базе данных то он будет создан."""

        lesson_data = validated_data.pop('lesson')
        course = Course.objects.create(**validated_data)

        for data in lesson_data:
            lesson_object, flag = Lesson.objects.get_or_create(title=data['title'],
                                                               defaults={
                                                                   'description': data['description'],
                                                                   'url_video': data['url_video'],
                                                               })
            course.lesson.add(lesson_object)

        return course

    def validate_lesson(self, data):
        """
        Метод валидирует данные по полю "Lesson".
        """
        errors = {}
        for lesson_object in data:
            if 'title' not in lesson_object.keys():
                errors['title'] = 'Обязательное поле'
            if 'description' not in lesson_object.keys():
                errors['description'] = 'Обязательное поле'
            if 'url_video' not in lesson_object.keys():
                errors['url_video'] = 'Обязательное поле'
            if errors:
                raise serializers.ValidationError(errors)
        return data

    def update(self, instance, validated_data):
        """
        Метод обновляет данные объекта модели Course в соответствие с запросом клиента.
        """
        instance.title = validated_data.get('title', instance.title)
        instance.picture = validated_data.get('picture', instance.picture)
        instance.description = validated_data.get('description', instance.description)

        lesson_data = validated_data.get('lesson')
        lesson_object_list = []

        for data in lesson_data:
            lesson_object, flag = Lesson.objects.get_or_create(title=data['title'],
                                                               defaults={
                                                                   'description': data['description'],
                                                                   'url_video': data['url_video'],
                                                               })
            lesson_object_list.append(lesson_object)

        instance.lesson.set(lesson_object_list)
        instance.save()

        return instance

    def get_count_lesson(self, instance):
        """Метод возвращает общее количество связанных полей lesson для текущего объекта Course."""

        return instance.lesson.count()


class CourseSerializerByLessonId(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('title', 'description', 'lesson',)
