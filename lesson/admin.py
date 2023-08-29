from django.contrib import admin

from lesson.models import Lesson


# Register your models here.
@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'description', 'url_video')
    list_display_links = ('title', 'url_video')
    search_fields = ('title', 'url_video')
    list_filter = ('pk', 'title')
