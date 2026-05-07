import requests
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.views import APIView
from rest_framework.response import Response



proxies = {
    "http": "http://host.docker.internal:10808",
    "https": "http://host.docker.internal:10808",
}

@method_decorator(cache_page(60 * 5), name="dispatch") # implement this decorator on dispatch method which handles requests and responses --> name="disatch"
class InfoExampleAPIView(APIView):

    def get(self, request):
        response = requests.get(
            "https://fe210ec8-8439-45dd-a38e-e502358113d1.mock.pstmn.io/weather",
            proxies=proxies,
        )
        return Response(response.json())