from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.utils import timezone
from courses.models import Course
from .models import Order, Payment
from .serializers import OrderSerializer, CreateOrderSerializer


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_order(request):
    """Создать заказ на покупку курса"""
    serializer = CreateOrderSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    course_id = serializer.validated_data['course_id']
    course = get_object_or_404(Course, id=course_id, is_active=True)
    
    # Проверка, не куплен ли уже курс
    if course.students.filter(id=request.user.id).exists():
        return Response(
            {'detail': 'Вы уже купили этот курс'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Создание заказа
    order = Order.objects.create(
        user=request.user,
        course=course,
        amount=course.price,
        status='pending'
    )
    
    return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def complete_payment(request, order_id):
    """
    Завершить оплату (mock для MVP)
    В реальном проекте здесь будет интеграция со Stripe
    """
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    if order.status == 'completed':
        return Response(
            {'detail': 'Заказ уже оплачен'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Mock оплаты - просто помечаем как оплаченный
    order.status = 'completed'
    order.save()
    
    # Создаём запись о платеже
    payment, created = Payment.objects.get_or_create(order=order)
    payment.paid = True
    payment.paid_at = timezone.now()
    payment.save()
    
    # Даём доступ к курсу
    order.course.students.add(request.user)
    
    return Response({
        'detail': 'Оплата прошла успешно',
        'order': OrderSerializer(order).data
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_orders(request):
    """Получить список заказов пользователя"""
    orders = Order.objects.filter(user=request.user)
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_courses(request):
    """Получить список купленных курсов"""
    courses = request.user.purchased_courses.all()
    from courses.serializers import CourseListSerializer
    serializer = CourseListSerializer(courses, many=True)
    return Response(serializer.data)
