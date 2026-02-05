from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Course(models.Model):
    """Модель курса"""
    title = models.CharField(max_length=200, verbose_name="Название")
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(verbose_name="Краткое описание")
    full_description = models.TextField(verbose_name="Полное описание")
    cover_image = models.ImageField(upload_to='courses/', verbose_name="Обложка", blank=True, null=True)
    banner_image = models.ImageField(upload_to='courses/banners/', verbose_name="Баннер", blank=True, null=True)
    
    # Категория и уровень
    category = models.CharField(max_length=100, verbose_name="Категория", blank=True)
    level = models.CharField(max_length=50, choices=[
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('pro', 'Pro'),
    ], default='beginner', verbose_name="Уровень")
    
    # Цена и доступ
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    access_type = models.CharField(max_length=50, choices=[
        ('lifetime', 'Пожизненный доступ'),
        ('monthly', 'Месячная подписка'),
        ('yearly', 'Годовая подписка'),
    ], default='lifetime', verbose_name="Тип доступа")
    
    # Дополнительные данные
    duration_hours = models.IntegerField(verbose_name="Длительность (часы)", default=0)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0, verbose_name="Рейтинг")
    reviews_count = models.IntegerField(default=0, verbose_name="Количество отзывов")
    
    # Преимущества курса (JSON)
    benefits = models.JSONField(default=list, verbose_name="Преимущества", blank=True)
    
    # Управление
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    has_certificate = models.BooleanField(default=False, verbose_name="Сертификат прохождения")
    students = models.ManyToManyField(User, related_name='purchased_courses', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    @property
    def lessons_count(self):
        return self.lessons.count()
    
    @property
    def total_duration_minutes(self):
        """Общая длительность всех уроков в минутах"""
        return sum(lesson.duration_minutes for lesson in self.lessons.all())


class Lesson(models.Model):
    """Модель урока"""
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=200, verbose_name="Название")
    order_index = models.IntegerField(default=0, verbose_name="Порядковый индекс")
    
    # Видео - можно загрузить файл или указать URL
    video_file = models.FileField(upload_to='lessons/videos/', verbose_name="Видео файл", blank=True, null=True)
    video_url = models.URLField(verbose_name="URL видео", blank=True)
    duration_minutes = models.IntegerField(verbose_name="Длительность (минуты)", default=0)
    
    # Формат видео
    VIDEO_FORMATS = [
        ('16:9', 'Горизонтальное (16:9)'),
        ('9:16', 'Вертикальное (9:16)'),
        ('1:1', 'Квадратное (1:1)'),
    ]
    video_format = models.CharField(max_length=10, choices=VIDEO_FORMATS, default='16:9', verbose_name="Формат видео")
    
    # Контент урока
    text_content = models.TextField(verbose_name="Текстовое описание", blank=True)
    
    # Таймкоды (JSON формат: [{"time": "00:00", "label": "Разминка"}, ...])
    timestamps = models.JSONField(default=list, verbose_name="Таймкоды", blank=True)
    
    # Ресурсы (JSON формат: [{"type": "pdf", "url": "...", "name": "..."}, ...])
    resources = models.JSONField(default=list, verbose_name="Файлы и ресурсы", blank=True)
    
    # Доступ
    is_free_preview = models.BooleanField(default=False, verbose_name="Бесплатный превью")
    preview_duration_seconds = models.IntegerField(default=120, verbose_name="Длительность превью (сек)")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
        ordering = ['order_index', 'created_at']
    
    def __str__(self):
        return f"{self.course.title} - {self.title}"
    
    def get_video_url(self):
        """Возвращает URL видео - либо загруженного файла, либо внешнего URL"""
        if self.video_file:
            return self.video_file.url
        return self.video_url


class LessonProgress(models.Model):
    """Прогресс пользователя по урокам"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lesson_progress')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='progress')
    completed = models.BooleanField(default=False, verbose_name="Завершён")
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name="Дата завершения")
    watch_time_seconds = models.IntegerField(default=0, verbose_name="Время просмотра (сек)")
    last_position_seconds = models.IntegerField(default=0, verbose_name="Последняя позиция (сек)")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('user', 'lesson')
        verbose_name = "Прогресс урока"
        verbose_name_plural = "Прогресс уроков"
    
    def __str__(self):
        return f"{self.user.email} - {self.lesson.title}"


class CourseReview(models.Model):
    """Отзывы о курсе"""
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='course_reviews')
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)], verbose_name="Рейтинг")
    comment = models.TextField(verbose_name="Комментарий", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('course', 'user')
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.email} - {self.course.title} ({self.rating}/5)"
