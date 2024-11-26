import json

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from checker.models import ScrapedData, Partner
from checker.serializers import ScrapedDataSerializer
from redis_client.redis_client import redis_client


class ComparingDataKtc(APIView):
    def get(self, request):
        try:
            data = ScrapedData.objects.all()
            serializer = ScrapedDataSerializer(data, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except ValueError as e:
            return Response(
                {"error": f"Value error occurred: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        except Exception as e:
            return Response(
                {"error": f"An unexpected error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class PartnerDataView(APIView):
    def get(self, request, slug):
        try:
            partner = Partner.objects.get(slug=slug)
            data = ScrapedData.objects.filter(partner=partner)
            serializer = ScrapedDataSerializer(data, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Partner.DoesNotExist:
            return Response(
                {"error": "Partner not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        except Exception as e:
            return Response(
                {"error": f"An unexpected error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)


