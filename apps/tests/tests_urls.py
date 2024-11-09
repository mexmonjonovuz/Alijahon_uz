import requests
from django.urls import reverse_lazy
from requests import request


class TestUrl:
    def test_main_urls(self):
        url = reverse_lazy('main_base')
        response = requests.get(url)
        assert response.status_code == 200
