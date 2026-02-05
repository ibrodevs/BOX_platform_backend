from rest_framework import serializers
from .models import ChatMessage


class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = ('id', 'message', 'response', 'created_at')
        read_only_fields = ('id', 'response', 'created_at')


class SendMessageSerializer(serializers.Serializer):
    message = serializers.CharField(max_length=1000)
