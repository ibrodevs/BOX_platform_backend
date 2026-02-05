from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import Course, Lesson, LessonProgress, CourseReview
from .serializers import (
    CourseListSerializer, 
    CourseDetailSerializer, 
    LessonSerializer,
    LessonProgressSerializer,
    CourseReviewSerializer
)


class CourseViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Course.objects.filter(is_active=True)
    permission_classes = (AllowAny,)
    lookup_field = 'slug'
    
    def get_serializer_class(self):
        if self.action == 'list':
            return CourseListSerializer
        return CourseDetailSerializer
    
    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def my_progress(self, request, slug=None):
        """Получить прогресс пользователя по курсу"""
        course = self.get_object()
        
        # Проверка доступа
        if not course.students.filter(id=request.user.id).exists():
            return Response(
                {'detail': 'У вас нет доступа к этому курсу'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        lessons = course.lessons.all()
        progress_data = []
        
        for lesson in lessons:
            try:
                progress = LessonProgress.objects.get(user=request.user, lesson=lesson)
                progress_data.append(LessonProgressSerializer(progress).data)
            except LessonProgress.DoesNotExist:
                progress_data.append({
                    'lesson': lesson.id,
                    'completed': False,
                    'completed_at': None,
                    'watch_time_seconds': 0
                })
        
        return Response(progress_data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_lesson(request, lesson_id):
    """Получить урок (только для купивших курс)"""
    lesson = get_object_or_404(Lesson, id=lesson_id)
    
    # Проверка доступа
    if not lesson.is_free:
        has_access = lesson.course.students.filter(id=request.user.id).exists()
        if not has_access:
            return Response(
                {'detail': 'Вы должны купить курс для доступа к этому уроку'},
                status=status.HTTP_403_FORBIDDEN
            )
    
    serializer = LessonSerializer(lesson, context={'request': request})
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_lesson_progress(request, lesson_id):
    """Обновить прогресс урока"""
    lesson = get_object_or_404(Lesson, id=lesson_id)
    
    # Проверка доступа
    has_access = lesson.course.students.filter(id=request.user.id).exists()
    if not has_access and not lesson.is_free_preview:
        return Response(
            {'detail': 'У вас нет доступа к этому уроку'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    progress, created = LessonProgress.objects.get_or_create(
        user=request.user,
        lesson=lesson
    )
    
    # Обновляем данные
    if 'completed' in request.data and request.data['completed']:
        progress.completed = True
        progress.completed_at = timezone.now()
    
    if 'watch_time_seconds' in request.data:
        progress.watch_time_seconds = request.data['watch_time_seconds']
    
    if 'last_position_seconds' in request.data:
        progress.last_position_seconds = request.data['last_position_seconds']
    
    progress.save()
    
    serializer = LessonProgressSerializer(progress)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_review(request, course_id):
    """Создать отзыв о курсе"""
    course = get_object_or_404(Course, id=course_id)
    
    # Проверка, что пользователь купил курс
    if not course.students.filter(id=request.user.id).exists():
        return Response(
            {'detail': 'Вы можете оставлять отзывы только о купленных курсах'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    # Проверка, есть ли уже отзыв
    if CourseReview.objects.filter(course=course, user=request.user).exists():
        return Response(
            {'detail': 'Вы уже оставили отзыв на этот курс'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    serializer = CourseReviewSerializer(data=request.data)
    if serializer.is_valid():
        review = serializer.save(user=request.user, course=course)
        
        # Обновляем рейтинг курса
        reviews = CourseReview.objects.filter(course=course)
        avg_rating = sum(r.rating for r in reviews) / reviews.count()
        course.rating = round(avg_rating, 2)
        course.reviews_count = reviews.count()
        course.save()
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_course_reviews(request, course_id):
    """Получить все отзывы курса"""
    course = get_object_or_404(Course, id=course_id)
    reviews = CourseReview.objects.filter(course=course).order_by('-created_at')
    serializer = CourseReviewSerializer(reviews, many=True)
    return Response(serializer.data)
