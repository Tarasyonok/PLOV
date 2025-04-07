import random

import django.core.management.base
import django.utils.timezone
import faker
import mocklms.models


class Command(django.core.management.base.BaseCommand):
    help = 'Creates real user profiles with interactive input'

    def handle(self, *args, **options):

        self.stdout.write(self.style.HTTP_INFO('\n🚀 Creating a new profile (press Enter for random values)'))

        profile = self.create_profile()
        course = self.create_course(profile)
        self.create_teachers(course)

        self.stdout.write(
            self.style.SUCCESS(f'✅ Created profile: {profile.display_name} ' f'(ID: {profile.lms_profile_id})')
        )

    def create_profile(self):
        fake = faker.Faker('ru_RU')

        lms_profile_id = input('Profile ID (unique number): ') or random.randint(100000, 999999)
        username = input('Username: ') or fake.user_name()
        gender = int(input('Gender (0 - male | 1 - female): ') or random.randint(0, 1))
        last_name = input('Last Name: ')
        if not last_name:
            last_name = [fake.last_name_male(), fake.last_name_female()][gender]

        first_name = input('First Name: ')
        if not first_name:
            first_name = [fake.first_name_male(), fake.first_name_female()][gender]

        middle_name = input('Middle Name: ')
        if not middle_name:
            middle_name = [fake.middle_name_male(), fake.middle_name_female()][gender]

        email = input('Email: ') or fake.email()
        phone = input('Phone (+7XXXXXXXXXX): ') or f'+79{fake.msisdn()[:9]}'
        birth_date = input('Birth Date (YYYY-MM-DD): ') or fake.date_of_birth(minimum_age=12, maximum_age=18).strftime(
            '%Y-%m-%d'
        )

        return mocklms.models.LMSProfile.objects.create(
            lms_profile_id=lms_profile_id,
            uid=random.randint(1000000000, 9999999999),
            username=username,
            last_name=last_name,
            first_name=first_name,
            middle_name=middle_name,
            gender=gender,
            display_name=f'{last_name} {first_name}',
            avatar='avatar_mock.jpg',
            email=email,
            phone=phone,
            birth_date=birth_date,
            city=fake.city_name(),
            school='Школа ' + fake.company(),
            school_class=f'{random.randint(5, 11)} класс',
        )

    def create_course(self, profile):
        title = 'Django | Специализации Яндекс Лицея | ' + input('Поток (пример: Весна 24/25): ') or 'Весна 24/25'
        rating = int(input('Rating: ') or random.randint(50, 150))
        has_certificate = random.choice([True, False])
        if has_certificate:
            certificate_id = random.randint(10000, 99999)
            certificate_number = random.randint(1000000000, 9999999999)
        else:
            certificate_id = None
            certificate_number = None

        course = mocklms.models.LMSCourse.objects.create(
            profile=profile,
            title=title,
            rating=rating,
            status=random.choice(['enrolled', 'graduated']),
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
