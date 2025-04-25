import django.core.management.base
import django.utils.timezone
import faker

import mocklms.models


class Command(django.core.management.base.BaseCommand):
    help = 'Создаёт фейковый профиль ученика в LMS'
    fake = faker.Faker('ru_RU')

    def handle(self, *args, **options):

        self.stdout.write(self.style.HTTP_INFO('\n🚀 Создаю профиль (нажмите Enter для случайных значений)'))

        profile = self.create_profile()
        course = self.create_course(profile)
        self.create_teachers(course)

        self.stdout.write(
            self.style.SUCCESS(f'✅ Создал профиль: {profile.display_name} (ID: {profile.lms_profile_id})'),
        )

    def create_profile(self):
        lms_profile_id = input('ID профиля (уникальный номер): ') or self.fake.pyint(100000, 999999)
        username = input('Логин: ') or self.fake.user_name()
        gender = input('Пол (0 - мужской | 1 - женский): ') or self.fake.pybool()
        last_name = input('Фамилия: ') or [self.fake.last_name_male(), self.fake.last_name_female()][gender]
        first_name = input('Имя: ') or [self.fake.first_name_male(), self.fake.first_name_female()][gender]
        middle_name = input('Отчество: ') or [self.fake.middle_name_male(), self.fake.middle_name_female()][gender]
        email = input('Email: ') or self.fake.email()
        phone = input('Телефон (+7XXXXXXXXXX): ') or f'+79{self.fake.msisdn()[:9]}'
        birth_date = input('Дата рождения (ГГГГ-ММ-ДД): ') or self.fake.date_of_birth(
            minimum_age=12,
            maximum_age=18,
        ).strftime('%Y-%m-%d')

        return mocklms.models.LMSProfile.objects.create(
            lms_profile_id=lms_profile_id,
            uid=self.fake.pyint(1000000000, 9999999999),
            username=username,
            last_name=last_name,
            first_name=first_name,
            middle_name=middle_name,
            gender=list(mocklms.models.LMSProfile.GenderChoices)[gender],
            display_name=f'{last_name} {first_name}',
            avatar='avatar_mock.jpg',
            email=email,
            phone=phone,
            birth_date=birth_date,
            city=self.fake.city_name(),
            school='Школа ' + self.fake.company(),
            school_class=f'{self.fake.pyint(5, 11)} класс',
        )

    def create_course(self, profile):
        title = 'Django | Специализации Яндекс Лицея | ' + input('Поток (пример: Весна 24/25): ') or 'Весна 24/25'
        rating = int(input('Рейтинг: ') or self.fake.pyint(50, 150))
        has_certificate = self.fake.pybool()
        if has_certificate:
            certificate_id = self.fake.pyint(10000, 99999)
            certificate_number = self.fake.pyint(1000000000, 9999999999)
        else:
            certificate_id = None
            certificate_number = None

        course = mocklms.models.LMSCourse.objects.create(
            profile=profile,
            title=title,
            rating=rating,
            status=['enrolled', 'graduated'][self.fake.pyint(0, 1)],
            certificate_id=certificate_id,
            certificate_number=certificate_number,
            accessibility_status='active',
        )

        mocklms.models.LMSGroup.objects.create(
            course=course,
            name=f'Группа для {course.title}',
            status=course.status,
        )

        return course

    def create_teachers(self, course):
        if not mocklms.models.LMSTeacher.objects.filter(display_name='Ерёмин Данила').exists():
            mocklms.models.LMSTeacher.objects.create(
                course=course,
                display_name='Ерёмин Данила',
                avatar='danila_avatar.jpg',
            )

        if not mocklms.models.LMSTeacher.objects.filter(display_name='Кашин Павел').exists():
            mocklms.models.LMSTeacher.objects.create(
                course=course,
                display_name='Кашин Павел',
                avatar='raccoon_avatar.jpg',
            )
