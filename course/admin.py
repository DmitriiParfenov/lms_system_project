from django.contrib import admin

from course.models import Course


# Register your models here.
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'user_course')
    list_display_links = ('title', )
    search_fields = ('title', )
    list_filter = ('title', )
