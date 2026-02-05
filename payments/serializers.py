from rest_framework import serializers
from .models import Order, Payment
from courses.serializers import CourseListSerializer


class OrderSerializer(serializers.ModelSerializer):
    course_details = CourseListSerializer(source='course', read_only=True)
    
    class Meta:
        model = Order
        fields = ('id', 'course', 'course_details', 'amount', 'status', 'created_at')
        read_only_fields = ('id', 'amount', 'status', 'created_at')


class CreateOrderSerializer(serializers.Serializer):
    course_id = serializers.IntegerField()
    
    def validate_course_id(self, value):
        from courses.models import Course
        try:
            course = Course.objects.get(id=value, is_active=True)
        except Course.DoesNotExist:
            raise serializers.ValidationError("Курс не найден")
        return value


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ('id', 'order', 'paid', 'paid_at')
