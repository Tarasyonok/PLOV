import mocklms.models
import mocklms.serializers
import rest_framework.generics


class ProfileDetailView(rest_framework.generics.RetrieveAPIView):
    queryset = mocklms.models.LMSProfile.objects.all()
    serializer_class = mocklms.serializers.ProfileSerializer
    lookup_field = 'lms_profile_id'
    lookup_url_kwarg = 'lms_profile_id'


class ProfileListView(rest_framework.generics.ListAPIView):
    queryset = mocklms.models.LMSProfile.objects.all()
    serializer_class = mocklms.serializers.ProfileSerializer
