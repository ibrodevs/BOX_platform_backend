from rest_framework import serializers
from .models import Course, Lesson, LessonProgress, CourseReview


class LessonProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonProgress
        fields = ('id', 'lesson', 'completed', 'completed_at', 'watch_time_seconds', 'last_position_seconds')


class LessonSerializer(serializers.ModelSerializer):
    progress = serializers.SerializerMethodField()
    video_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Lesson
        fields = ('id', 'title', 'order_index', 'video_url', 'video_format', 'duration_minutes', 
                  'text_content', 'timestamps', 'resources', 'is_free_preview', 
                  'preview_duration_seconds', 'progress')
    
    def get_video_url(self, obj):
        """Возвращает URL видео"""
        request = self.context.get('request')
        video_url = obj.get_video_url()
        
        # Если это относительный URL (загруженный файл), делаем абсолютным
        if video_url and request and not video_url.startswith('http'):
            return request.build_absolute_uri(video_url)
        return video_url
    
    def get_progress(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            try:
                progress = LessonProgress.objects.get(user=request.user, lesson=obj)
                return LessonProgressSerializer(progress).data
            except LessonProgress.DoesNotExist:
                return None
        return None
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get('request')
        
        # Если урок не бесплатный превью и пользователь не купил курс - ограничить доступ
        if request and not instance.is_free_preview:
            user = request.user
            if user.is_authenticated:
                has_access = instance.course.students.filter(id=user.id).exists()
                if not has_access:
                    data['video_url'] = None
                    data['text_content'] = data['text_content'][:200] + '...' if data['text_content'] else ''
                    data['resources'] = []
            else:
                data['video_url'] = None
                data['text_content'] = data['text_content'][:200] + '...' if data['text_content'] else ''
                data['resources'] = []
        
        return data


class CourseReviewSerializer(serializers.ModelSerializer):
    user_email = serializers.CharField(source='user.email', read_only=True)
    user_name = serializers.SerializerMethodField()
    
    class Meta:
        model = CourseReview
        fields = ('id', 'user_email', 'user_name', 'rating', 'comment', 'created_at')
    
    def get_user_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}".strip() or obj.user.email.split('@')[0]


class CourseListSerializer(serializers.ModelSerializer):
    lessons_count = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Course
        fields = ('id', 'title', 'slug', 'description', 'cover_image', 'price', 'duration_hours', 
                  'level', 'category', 'rating', 'reviews_count', 'lessons_count', 'access_type')


class CourseDetailSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)
    lessons_count = serializers.IntegerField(read_only=True)
    total_duration_minutes = serializers.IntegerField(read_only=True)
    is_purchased = serializers.SerializerMethodField()
    user_progress = serializers.SerializerMethodField()
    reviews = CourseReviewSerializer(many=True, read_only=True)
    
    class Meta:
        model = Course
        fields = ('id', 'title', 'slug', 'description', 'full_description', 'cover_image', 
                  'banner_image', 'price', 'duration_hours', 'level', 'category', 'rating', 
                  'reviews_count', 'benefits', 'access_type', 'has_certificate', 
                  'lessons_count', 'total_duration_minutes', 'lessons', 'is_purchased', 
                  'user_progress', 'reviews', 'created_at')
    
    def get_is_purchased(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.students.filter(id=request.user.id).exists()
        return False
    
    def get_user_progress(self, obj):
        """Прогресс пользователя по курсу"""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            total_lessons = obj.lessons.count()
            if total_lessons == 0:
                return {'completed': 0, 'total': 0, 'percentage': 0}
            
            completed_lessons = LessonProgress.objects.filter(
                user=request.user,
                lesson__course=obj,
                completed=True
            ).count()
            
            return {
                'completed': completed_lessons,
                'total': total_lessons,
                'percentage': round((completed_lessons / total_lessons) * 100, 2)
            }
        return None


class LessonProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonProgress
        fields = ('lesson', 'completed', 'completed_at', 'watch_time_seconds')
