from rest_framework import serializers

from course.models import Course
from lesson.models import Lesson
from lesson.serializers import LessonSerializer


class CourseSerializer(serializers.ModelSerializer):
    """Класс сериализут поля модели Course: <title>, <description>. Поле <lesson> сериализуется через вложенный
    сериализатор LessonSerializer с полным описанием полей вложенного сериализатора, при чем, если при создании
    объекта модели Course и при описании всех полей вложенного сериализатора для Lesson не существует объекта
    модели Lesson, то он будет создан. Поле <count_lesson> — это общее количество уроков в курсе."""

    lesson = LessonSerializer(many=True)
    count_lesson = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ('title', 'description', 'count_lesson', 'lesson',)

    def create(self, validated_data):
        """Метод создает объект модели Course с указанием полей для вложенного объекта модели Lesson. Если текущий
        объект есть в базе данных, будет возбуждено исключение о существование такого объекта, если нет, то будет
        создан объект модели Lesson."""

        lesson_data = validated_data.pop('lesson')
        course = Course.objects.create(**validated_data)

        for data in lesson_data:
            lesson_object = Lesson.objects.create(**data)
            course.lesson.add(lesson_object)

        return course

    def get_count_lesson(self, instance):
        """Метод возвращает общее количество связанных полей lesson для текущего объекта Course."""
        return instance.lesson.count()


class CourseSerializerByLessonId(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('title', 'description', 'lesson',)
