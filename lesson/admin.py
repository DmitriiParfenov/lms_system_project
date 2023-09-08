from django.contrib import admin

from lesson.models import Lesson


# Register your models here.
@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'url_video', 'user_lesson')
    list_display_links = ('title', 'url_video')
    search_fields = ('title', 'url_video')
    list_filter = ('title', )
