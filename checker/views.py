# views.py
from rest_framework.views import APIView
from rest_framework.response import Response

from stores.KTC.ktc import start_ktc_wacom
from .models import ScrapedData
from .serializers import ScrapedDataSerializer

class ScrapedDataView(APIView):
    def get(self, request):
        data = start_ktc_wacom()
        return Response(data=data)
