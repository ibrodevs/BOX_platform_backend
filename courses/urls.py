from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'', views.CourseViewSet, basename='course')

urlpatterns = [
    path('lessons/<int:lesson_id>/', views.get_lesson, name='get_lesson'),
    path('lessons/<int:lesson_id>/progress/', views.update_lesson_progress, name='update_progress'),
    path('<int:course_id>/reviews/', views.get_course_reviews, name='course_reviews'),
    path('<int:course_id>/reviews/create/', views.create_review, name='create_review'),
    path('', include(router.urls)),
]
