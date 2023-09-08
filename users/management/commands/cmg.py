from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management import BaseCommand

from course.models import Course
from lesson.models import Lesson


class Command(BaseCommand):
    def handle(self, *args, **options):
        group_manager = Group.objects.create(name='Moderator')
        content_type_1 = ContentType.objects.get_for_model(Course)
        content_type_2 = ContentType.objects.get_for_model(Lesson)

        permission_course_view, __ = Permission.objects.get_or_create(codename='view_course',
                                                                      content_type=content_type_1)
        group_manager.permissions.add(permission_course_view)

        permission_change_course, __ = Permission.objects.get_or_create(codename='change_course',
                                                                        content_type=content_type_1)
        group_manager.permissions.add(permission_change_course)

        permission_change_lesson, __ = Permission.objects.get_or_create(codename='change_lesson',
                                                                        content_type=content_type_2)
        group_manager.permissions.add(permission_change_lesson)

        permission_view_lesson, __ = Permission.objects.get_or_create(codename='view_lesson',
                                                                      content_type=content_type_2)
        group_manager.permissions.add(permission_view_lesson)
