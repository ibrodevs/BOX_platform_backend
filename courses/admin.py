from django.contrib import admin
from .models import Course, Lesson, LessonProgress, CourseReview


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'level', 'category', 'price', 'rating', 'reviews_count', 'is_active', 'created_at')
    list_filter = ('level', 'category', 'is_active', 'access_type')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('students',)


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order_index', 'duration_minutes', 'video_format', 'is_free_preview')
    list_filter = ('course', 'is_free_preview', 'video_format')
    search_fields = ('title', 'course__title')
    ordering = ('course', 'order_index')
    fieldsets = (
        ('Основная информация', {
            'fields': ('course', 'title', 'order_index', 'text_content')
        }),
        ('Видео', {
            'fields': ('video_file', 'video_url', 'video_format', 'duration_minutes'),
            'description': 'Загрузите видео файл или укажите URL. Выберите формат видео.'
        }),
        ('Дополнительный контент', {
            'fields': ('timestamps', 'resources'),
            'classes': ('collapse',)
        }),
        ('Настройки доступа', {
            'fields': ('is_free_preview', 'preview_duration_seconds')
        }),
    )


@admin.register(LessonProgress)
class LessonProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'lesson', 'completed', 'watch_time_seconds', 'completed_at')
    list_filter = ('completed', 'lesson__course')
    search_fields = ('user__email', 'lesson__title')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(CourseReview)
class CourseReviewAdmin(admin.ModelAdmin):
    list_display = ('course', 'user', 'rating', 'created_at')
    list_filter = ('rating', 'course')
    search_fields = ('user__email', 'course__title', 'comment')
    readonly_fields = ('created_at', 'updated_at')
