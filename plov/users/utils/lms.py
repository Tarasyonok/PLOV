import django.conf
import requests


class LMSClient:
    def __init__(self):
        self.base_url = django.conf.settings.LMS_API_URL

    def get_profile(self, profile_id):
        url = self.base_url + f'/profiles/{profile_id}'
        response = requests.get(
            url,
            timeout=10,
        )
        response.raise_for_status()
        return response.json()
