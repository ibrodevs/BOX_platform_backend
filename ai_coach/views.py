import google.generativeai as genai
from django.conf import settings
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import ChatMessage
from .serializers import ChatMessageSerializer, SendMessageSerializer


# Настройка Gemini
if settings.GEMINI_API_KEY:
    genai.configure(api_key=settings.GEMINI_API_KEY)


SYSTEM_PROMPT = """
Ты - AI тренер по боксу. Твоя задача - помогать ученикам платформы онлайн-курсов бокса.

Твоя роль:
- Отвечай на вопросы о технике бокса
- Объясняй основы и продвинутые концепции
- Давай советы по тренировкам
- Помогай с мотивацией
- Отвечай на вопросы о платформе

Что НЕ делать:
- НЕ давай медицинские советы
- НЕ диагностируй травмы
- Если вопрос о здоровье - советуй обратиться к врачу

Стиль общения:
- Мотивирующий и энергичный
- Профессиональный, но дружелюбный
- КРАТКИЕ И ПОНЯТНЫЕ ОТВЕТЫ (максимум 3-5 предложений)
- Используй терминологию бокса
- Конкретика без лишних слов
- Структурируй ответ: 1-2 ключевых момента
- Добавляй короткие практические советы

ВАЖНО: Ответы должны быть средней длины - не слишком короткие, но и не длинные. 
Оптимально: 2-4 абзаца по 1-2 предложения в каждом.

Всегда отвечай на русском языке.
"""


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_message(request):
    """Отправить сообщение AI тренеру"""
    serializer = SendMessageSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    user_message = serializer.validated_data['message']
    
    # Проверка лимита сообщений (опционально для MVP)
    daily_messages = ChatMessage.objects.filter(
        user=request.user,
        created_at__date=timezone.now().date()
    ).count()
    
    if daily_messages >= 50:  # Лимит 50 сообщений в день
        return Response(
            {'detail': 'Достигнут дневной лимит сообщений'},
            status=status.HTTP_429_TOO_MANY_REQUESTS
        )
    
    try:
        # Вызов Gemini API
        if not settings.GEMINI_API_KEY:
            ai_response = "AI тренер временно недоступен. Пожалуйста, настройте GEMINI_API_KEY."
        else:
            # Используем gemini-2.5-flash - более быстрая модель
            model = genai.GenerativeModel('gemini-2.5-flash')
            
            # Формируем полный промпт
            full_prompt = f"{SYSTEM_PROMPT}\n\nВопрос ученика: {user_message}\n\nОтвет:"
            
            response = model.generate_content(full_prompt)
            ai_response = response.text
        
        # Сохраняем в БД
        chat_message = ChatMessage.objects.create(
            user=request.user,
            message=user_message,
            response=ai_response
        )
        
        return Response(ChatMessageSerializer(chat_message).data)
    
    except Exception as e:
        error_message = str(e)
        # Проверяем тип ошибки
        if '429' in error_message or 'quota' in error_message.lower():
            ai_response = "⚠️ Превышен лимит запросов к AI. Пожалуйста, попробуйте позже или обратитесь к администратору."
        elif '404' in error_message:
            ai_response = "⚠️ Модель AI недоступна. Обратитесь к администратору."
        else:
            ai_response = f"⚠️ Произошла ошибка. Пожалуйста, попробуйте позже."
        
        # Сохраняем сообщение с ошибкой
        chat_message = ChatMessage.objects.create(
            user=request.user,
            message=user_message,
            response=ai_response
        )
        
        return Response(ChatMessageSerializer(chat_message).data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_chat_history(request):
    """Получить историю чата пользователя"""
    messages = ChatMessage.objects.filter(user=request.user)[:50]  # Последние 50
    serializer = ChatMessageSerializer(messages, many=True)
    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def clear_chat_history(request):
    """Очистить историю чата"""
    ChatMessage.objects.filter(user=request.user).delete()
    return Response({'detail': 'История чата очищена'})


from django.utils import timezone
