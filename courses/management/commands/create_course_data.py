"""
Management command для создания тестовых данных курсов
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from courses.models import Course, Lesson

User = get_user_model()


class Command(BaseCommand):
    help = 'Создать тестовые данные для курсов'

    def handle(self, *args, **kwargs):
        self.stdout.write('Создание тестовых курсов...')

        # Курс 1: Основы бокса
        course1, created = Course.objects.get_or_create(
            slug='basics-for-beginners',
            defaults={
                'title': 'Основы бокса для начинающих',
                'description': 'Изучите базовые техники бокса: стойка, передвижения, прямые удары',
                'full_description': '''Этот курс создан для тех, кто только начинает свой путь в боксе. 
                
Вы научитесь:
- Правильной боевой стойке
- Базовым передвижениям в ринге
- Прямым ударам (джеб и кросс)
- Работе с тенью
- Основам защиты

Курс включает 12 подробных видео-уроков с пошаговыми объяснениями каждой техники.''',
                'category': 'Техника',
                'level': 'beginner',
                'price': 2990,
                'duration_hours': 3,
                'rating': 4.8,
                'reviews_count': 156,
                'benefits': [
                    'Правильная постановка техники с нуля',
                    'Видео в HD качестве',
                    'Пожизненный доступ к материалам',
                    'Поддержка от команды'
                ],
                'access_type': 'lifetime',
                'has_certificate': True,
                'is_active': True
            }
        )

        if created:
            # Создаем уроки для курса 1
            lessons_data = [
                {
                    'title': 'Боевая стойка и баланс',
                    'order_index': 0,
                    'duration_minutes': 12,
                    'text_content': 'В этом уроке вы изучите правильную боевую стойку - основу всех техник бокса. Мы разберем позицию ног, распределение веса, положение рук и корпуса.',
                    'timestamps': [
                        {'time': '00:00', 'label': 'Введение'},
                        {'time': '01:30', 'label': 'Позиция ног'},
                        {'time': '04:20', 'label': 'Положение рук'},
                        {'time': '07:45', 'label': 'Распределение веса'},
                        {'time': '10:00', 'label': 'Практика'},
                    ],
                    'is_free_preview': True,
                    'video_url': 'https://example.com/lesson1.mp4'
                },
                {
                    'title': 'Базовые передвижения',
                    'order_index': 1,
                    'duration_minutes': 15,
                    'text_content': 'Научитесь двигаться в ринге правильно: вперед, назад, в стороны. Сохраняя баланс и готовность к атаке.',
                    'timestamps': [
                        {'time': '00:00', 'label': 'Шаги вперед'},
                        {'time': '05:00', 'label': 'Шаги назад'},
                        {'time': '09:30', 'label': 'Боковые перемещения'},
                        {'time': '12:00', 'label': 'Комбинации движений'},
                    ],
                    'is_free_preview': False,
                    'video_url': 'https://example.com/lesson2.mp4'
                },
                {
                    'title': 'Прямой удар - Джеб',
                    'order_index': 2,
                    'duration_minutes': 18,
                    'text_content': 'Джеб - самый важный удар в боксе. Разберем технику выполнения, типичные ошибки и способы тренировки.',
                    'timestamps': [
                        {'time': '00:00', 'label': 'Механика джеба'},
                        {'time': '06:00', 'label': 'Работа кулака'},
                        {'time': '11:00', 'label': 'Возврат руки'},
                        {'time': '15:00', 'label': 'Типичные ошибки'},
                    ],
                    'resources': [
                        {'type': 'pdf', 'name': 'Чек-лист техники джеба', 'url': 'https://example.com/jab-checklist.pdf'}
                    ],
                    'video_url': 'https://example.com/lesson3.mp4'
                },
            ]

            for lesson_data in lessons_data:
                Lesson.objects.create(course=course1, **lesson_data)

            self.stdout.write(self.style.SUCCESS(f'✓ Создан курс: {course1.title}'))

        # Курс 2: Продвинутая техника
        course2, created = Course.objects.get_or_create(
            slug='advanced-punches',
            defaults={
                'title': 'Продвинутая техника ударов',
                'description': 'Развитие силы и скорости ударов. Боковые, апперкоты, комбинации',
                'full_description': '''Курс для боксёров среднего уровня, желающих усовершенствовать технику ударов.
                
В программе:
- Боковые удары (хуки)
- Апперкоты
- Комбинации из 3-4 ударов
- Работа над силой удара
- Скоростные комбинации
                
16 уроков с детальным разбором каждой техники.''',
                'category': 'Техника',
                'level': 'intermediate',
                'price': 4990,
                'duration_hours': 5,
                'rating': 4.9,
                'reviews_count': 98,
                'benefits': [
                    'Улучшение техники ударов',
                    'Развитие силы и скорости',
                    'Изучение комбинаций',
                    'Разбор ошибок'
                ],
                'access_type': 'lifetime',
                'has_certificate': True,
                'is_active': True
            }
        )

        if created:
            self.stdout.write(self.style.SUCCESS(f'✓ Создан курс: {course2.title}'))

        # Курс 3: Защита и контратаки
        course3, created = Course.objects.get_or_create(
            slug='defense-counterattacks',
            defaults={
                'title': 'Защита и контратаки',
                'description': 'Научитесь защищаться и проводить эффективные контратаки',
                'full_description': '''Мастер-класс по оборонительным техникам и контратакам от Дмитрия Бивола.
                
Программа включает:
- Блоки и парирование
- Уклоны и нырки
- Работа корпусом
- Контратаки после защиты
- Тактика оборонительного боя
                
14 уроков с практическими упражнениями.''',
                'category': 'Защита',
                'level': 'intermediate',
                'price': 4990,
                'duration_hours': 4,
                'rating': 4.7,
                'reviews_count': 73,
                'benefits': [
                    'Надёжная защита',
                    'Эффективные контратаки',
                    'Улучшение рефлексов',
                    'Тактическое мышление'
                ],
                'access_type': 'lifetime',
                'has_certificate': False,
                'is_active': True
            }
        )

        if created:
            self.stdout.write(self.style.SUCCESS(f'✓ Создан курс: {course3.title}'))

        # Курс 4: Работа на мешке
        course4, created = Course.objects.get_or_create(
            slug='bag-work',
            defaults={
                'title': 'Работа на мешке',
                'description': 'Техника и выносливость при работе с боксёрским мешком',
                'full_description': '''Полный курс по работе с боксёрским мешком.
                
Программа:
- Правильная постановка ударов на мешке
- Отработка комбинаций
- Развитие выносливости
- Работа на скорость
- Силовые упражнения
                
10 практических уроков с детальными разборами.''',
                'category': 'Тренировки',
                'level': 'beginner',
                'price': 2990,
                'duration_hours': 3,
                'rating': 4.6,
                'reviews_count': 89,
                'benefits': [
                    'Улучшение техники ударов',
                    'Развитие выносливости',
                    'Увеличение силы',
                    'Кардио тренировка'
                ],
                'access_type': 'lifetime',
                'has_certificate': False,
                'is_active': True
            }
        )

        if created:
            self.stdout.write(self.style.SUCCESS(f'✓ Создан курс: {course4.title}'))

        # Курс 5: Спарринг
        course5, created = Course.objects.get_or_create(
            slug='sparring-tactics',
            defaults={
                'title': 'Спарринг: тактика и стратегия',
                'description': 'Подготовка к спаррингу. Тактика боя, чтение противника',
                'full_description': '''Продвинутый курс для подготовки к реальному бою.
                
Вы научитесь:
- Читать действия противника
- Тактике ведения боя
- Психологической подготовке
- Работе в различных стилях
- Адаптации под разных соперников
                
20 уроков от профессионала с мировым опытом.''',
                'category': 'Спарринг',
                'level': 'pro',
                'price': 6990,
                'duration_hours': 8,
                'rating': 5.0,
                'reviews_count': 45,
                'benefits': [
                    'Тактическое мышление',
                    'Чтение соперника',
                    'Адаптивность в бою',
                    'Психологическая подготовка'
                ],
                'access_type': 'lifetime',
                'has_certificate': True,
                'is_active': True
            }
        )

        if created:
            self.stdout.write(self.style.SUCCESS(f'✓ Создан курс: {course5.title}'))

        # Курс 6: Кондиция
        course6, created = Course.objects.get_or_create(
            slug='boxing-conditioning',
            defaults={
                'title': 'Кондиция боксёра',
                'description': 'Физическая подготовка: выносливость, сила, скорость',
                'full_description': '''Комплексная программа физической подготовки боксёра.
                
Включает:
- Кардио тренировки
- Силовые упражнения
- Развитие скорости
- Гибкость и координация
- Восстановление
                
15 тренировок для максимальной физической формы.''',
                'category': 'Физподготовка',
                'level': 'beginner',
                'price': 3490,
                'duration_hours': 4,
                'rating': 4.7,
                'reviews_count': 112,
                'benefits': [
                    'Улучшение выносливости',
                    'Увеличение силы',
                    'Развитие скорости',
                    'Общая физическая форма'
                ],
                'access_type': 'lifetime',
                'has_certificate': False,
                'is_active': True
            }
        )

        if created:
            self.stdout.write(self.style.SUCCESS(f'✓ Создан курс: {course6.title}'))

        self.stdout.write(self.style.SUCCESS('\n✓ Тестовые данные успешно созданы!'))
        self.stdout.write(f'Всего курсов в базе: {Course.objects.count()}')
