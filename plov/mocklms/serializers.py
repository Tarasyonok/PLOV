# Можно mixedCase, чтобы скопировать API LMS
# flake8: noqa: N815
import rest_framework.serializers

import mocklms.models


class TeacherSerializer(rest_framework.serializers.ModelSerializer):
    id = rest_framework.serializers.IntegerField()
    displayName = rest_framework.serializers.CharField(source='display_name')

    class Meta:
        model = mocklms.models.LMSTeacher
        fields = ['id', 'displayName', 'avatar']


class CourseSerializer(rest_framework.serializers.ModelSerializer):
    id = rest_framework.serializers.IntegerField()
    teachersList = TeacherSerializer(source='teachers_list', many=True)
    certificateId = rest_framework.serializers.IntegerField(source='certificate_id', allow_null=True)
    certificateNumber = rest_framework.serializers.CharField(source='certificate_number', allow_null=True)

    class Meta:
        model = mocklms.models.LMSCourse
        fields = [
            'id',
            'title',
            'teachersList',
            'group',
            'rating',
            'status',
            'certificateId',
            'certificateNumber',
        ]


class ProfileSerializer(rest_framework.serializers.ModelSerializer):
    profile = rest_framework.serializers.SerializerMethodField()
    coursesSummary = rest_framework.serializers.SerializerMethodField()

    def get_profile(self, obj):
        return {
            'id': obj.lms_profile_id,
            'uid': obj.uid,
            'username': obj.username,
            'isActive': obj.is_active,
            'lastName': obj.last_name,
            'firstName': obj.first_name,
            'middleName': obj.middle_name,
            'gender': obj.gender,
            'displayName': obj.display_name,
            'avatar': obj.avatar,
            'email': obj.email,
            'phone': obj.phone,
            'birthDate': obj.birth_date.strftime('%Y-%m-%d'),
            'city': obj.city,
            'school': obj.school,
            'schoolClass': obj.school_class,
            'tags': obj.tags,
            'clubs': obj.clubs,
            'competitions': obj.competitions,
        }

    def get_coursesSummary(self, obj):
        return {
            'student': CourseSerializer(obj.courses.all(), many=True).data,
            'teacher': [],
        }

    class Meta:
        model = mocklms.models.LMSProfile
        fields = ['profile', 'coursesSummary']
