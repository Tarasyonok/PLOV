import django.db.models


class LMSProfile(django.db.models.Model):
    lms_profile_id = django.db.models.IntegerField(unique=True)
    uid = django.db.models.BigIntegerField(unique=True)
    username = django.db.models.CharField(max_length=150)
    is_active = django.db.models.BooleanField(default=True)
    last_name = django.db.models.CharField(max_length=150)
    first_name = django.db.models.CharField(max_length=150)
    middle_name = django.db.models.CharField(max_length=150, blank=True, null=True)
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]
    gender = django.db.models.CharField(max_length=10, choices=GENDER_CHOICES)
    display_name = django.db.models.CharField(max_length=255)
    avatar = django.db.models.CharField(max_length=255, blank=True)
    email = django.db.models.EmailField()
    phone = django.db.models.CharField(max_length=20)
    birth_date = django.db.models.DateField()
    city = django.db.models.CharField(max_length=100, blank=True)
    school = django.db.models.CharField(max_length=255, blank=True)
    school_class = django.db.models.CharField(max_length=50, blank=True)
    tags = django.db.models.JSONField(default=list)
    clubs = django.db.models.JSONField(default=list)
    competitions = django.db.models.JSONField(default=list)
    public_key = django.db.models.TextField(blank=True)


class LMSCourse(django.db.models.Model):
    COURSE_STATUS = [
        ('enrolled', 'Enrolled'),
        ('graduated', 'Graduated'),
        ('dropped', 'Dropped'),
    ]
    profile = django.db.models.ForeignKey(
        'mocklms.LMSProfile',
        on_delete=django.db.models.CASCADE,
        related_name='courses',
    )
    title = django.db.models.CharField(max_length=255)
    rating = django.db.models.FloatField()
    events_count = django.db.models.IntegerField(default=0)
    visited_attendances_count = django.db.models.IntegerField(default=0)
    status = django.db.models.CharField(max_length=20, choices=COURSE_STATUS)
    certificate_id = django.db.models.IntegerField(null=True, blank=True)
    certificate_number = django.db.models.CharField(max_length=50, null=True, blank=True)
    accessibility_status = django.db.models.CharField(max_length=20)


class LMSGroup(django.db.models.Model):
    course = django.db.models.OneToOneField(
        'mocklms.LMSCourse',
        on_delete=django.db.models.CASCADE,
        related_name='group',
    )
    name = django.db.models.CharField(max_length=255)
    status = django.db.models.CharField(max_length=20)


class LMSTeacher(django.db.models.Model):
    course = django.db.models.ForeignKey(
        'mocklms.LMSCourse',
        on_delete=django.db.models.CASCADE,
        related_name='teachers_list',
    )
    display_name = django.db.models.CharField(max_length=255)
    avatar = django.db.models.CharField(max_length=255, blank=True)
