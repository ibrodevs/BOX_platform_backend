"""
Management command для создания тестовых данных
Использование: python manage.py create_test_data
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from courses.models import Course, Lesson

User = get_user_model()


class Command(BaseCommand):
    help = 'Создать тестовые данные для демо'

    def handle(self, *args, **kwargs):
        self.stdout.write('Создание тестовых данных...')

        # Создать тестового пользователя
        if not User.objects.filter(username='demo').exists():
            user = User.objects.create_user(
                username='demo',
                email='demo@boxer.com',
                password='demo123',
                first_name='Иван',
                last_name='Демонстрация'
            )
            self.stdout.write(self.style.SUCCESS('✅ Создан пользователь: demo / demo123'))
        else:
            user = User.objects.get(username='demo')
            self.stdout.write('⚠️  Пользователь demo уже существует')

        # Курс 1: Основы бокса
        if not Course.objects.filter(slug='osnovy-boksa').exists():
            course1 = Course.objects.create(
                title='Основы бокса для начинающих',
                slug='osnovy-boksa',
                description='Изучите фундаментальные техники бокса с нуля',
                full_description='''Этот курс создан специально для тех, кто никогда не занимался боксом.

Вы научитесь:
• Правильной стойке и перемещениям
• Базовым ударам (джеб, кросс, хук, апперкот)
• Защитным техникам
• Работе на груше и лапах

Курс состоит из 10 практических уроков с детальными объяснениями каждой техники.''',
                price=2990.00,
                duration_hours=8,
                level='beginner',
                is_active=True
            )

            # Уроки для курса 1
            lessons_data = [
                ('Введение и стойка', 30, 1, True),
                ('Базовая работа ног', 45, 2, False),
                ('Джеб - прямой удар', 40, 3, False),
                ('Кросс - силовой удар', 45, 4, False),
                ('Боковой удар - хук', 50, 5, False),
                ('Удар снизу - апперкот', 45, 6, False),
                ('Защита: блоки и уклоны', 55, 7, False),
                ('Комбинации ударов', 60, 8, False),
                ('Работа на мешке', 50, 9, False),
                ('Спарринг-подготовка', 55, 10, False),
            ]

            for title, duration, order, is_free in lessons_data:
                Lesson.objects.create(
                    course=course1,
                    title=title,
                    description=f'Подробный урок о теме: {title}',
                    video_url='https://www.youtube.com/embed/dQw4w9WgXcQ',
                    duration_minutes=duration,
                    order=order,
                    is_free=is_free
                )

            self.stdout.write(self.style.SUCCESS(f'✅ Создан курс: {course1.title}'))
        else:
            self.stdout.write('⚠️  Курс "Основы бокса" уже существует')

        # Курс 2: Продвинутая техника
        if not Course.objects.filter(slug='prodvinutaya-tehnika').exists():
            course2 = Course.objects.create(
                title='Продвинутая техника бокса',
                slug='prodvinutaya-tehnika',
                description='Освойте сложные техники и тактики профессионалов',
                full_description='''Курс для боксёров с опытом, готовых перейти на новый уровень.

В программе:
• Сложные комбинации
• Работа на разных дистанциях
• Контратака и тайминг
• Психология боя
• Тактическая подготовка

Этот курс поднимет ваш бокс на профессиональный уровень.''',
                price=4990.00,
                duration_hours=12,
                level='advanced',
                is_active=True
            )

            lessons_data = [
                ('Продвинутая работа ног', 60, 1, False),
                ('Углы и позиционирование', 65, 2, False),
                ('Сложные комбинации', 70, 3, False),
                ('Бой на средней дистанции', 60, 4, False),
                ('Ближний бой', 65, 5, False),
                ('Контратака', 70, 6, False),
                ('Тайминг и ритм', 60, 7, False),
                ('Защита высокого уровня', 65, 8, False),
                ('Психология боя', 55, 9, False),
                ('Тактическая подготовка', 70, 10, False),
            ]

            for title, duration, order, is_free in lessons_data:
                Lesson.objects.create(
                    course=course2,
                    title=title,
                    description=f'Продвинутый урок: {title}',
                    video_url='https://www.youtube.com/embed/kJQP7kiw5Fk',
                    duration_minutes=duration,
                    order=order,
                    is_free=is_free
                )

            self.stdout.write(self.style.SUCCESS(f'✅ Создан курс: {course2.title}'))
        else:
            self.stdout.write('⚠️  Курс "Продвинутая техника" уже существует')

        # Курс 3: Физическая подготовка
        if not Course.objects.filter(slug='fizicheskaya-podgotovka').exists():
            course3 = Course.objects.create(
                title='Физическая подготовка боксёра',
                slug='fizicheskaya-podgotovka',
                description='Силовые и кардио тренировки для боксёров',
                full_description='''Специализированная программа физической подготовки.

Что включено:
• Кардио выносливость
• Взрывная сила
• Функциональные тренировки
• Растяжка и мобильность
• Программа питания (бонус)

Станьте сильнее, быстрее и выносливее!''',
                price=3490.00,
                duration_hours=10,
                level='intermediate',
                is_active=True
            )

            lessons_data = [
                ('Оценка физической формы', 40, 1, True),
                ('Кардио для боксёров', 60, 2, False),
                ('Взрывная сила', 55, 3, False),
                ('Функциональные упражнения', 65, 4, False),
                ('Работа с весами', 60, 5, False),
                ('Плиометрика', 50, 6, False),
                ('Гибкость и растяжка', 45, 7, False),
                ('Программа тренировок', 70, 8, False),
            ]

            for title, duration, order, is_free in lessons_data:
                Lesson.objects.create(
                    course=course3,
                    title=title,
                    description=f'Тренировка: {title}',
                    video_url='https://www.youtube.com/embed/9bZkp7q19f0',
                    duration_minutes=duration,
                    order=order,
                    is_free=is_free
                )

            self.stdout.write(self.style.SUCCESS(f'✅ Создан курс: {course3.title}'))
        else:
            self.stdout.write('⚠️  Курс "Физическая подготовка" уже существует')

        self.stdout.write(self.style.SUCCESS('\n🎉 Тестовые данные созданы успешно!'))
        self.stdout.write('\nТеперь можно:')
        self.stdout.write('1. Войти как demo / demo123')
        self.stdout.write('2. Просмотреть 3 курса в каталоге')
        self.stdout.write('3. Попробовать бесплатные превью уроки')
        self.stdout.write('4. Купить курс и получить полный доступ\n')
