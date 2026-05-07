import requests
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.views import APIView
from rest_framework.response import Response



proxies = {
    "http": "http://host.docker.internal:10808",
    "https": "http://host.docker.internal:10808",
}

params = {
    "lat": 33.44,
    "lon": -94.04,
    "appid": "306b5dd93fe07aa6292e721861a95055",
}

@method_decorator(cache_page(60 * 20), name="dispatch") # implement this decorator on dispatch method which handles requests and responses --> name="disatch"
class InfoExampleAPIView(APIView):

    def get(self, request):
        response = requests.get(
            "https://api.openweathermap.org/data/2.5/weather",
            params=params,
            proxies=proxies,
        )
        return Response(response.json())