import json

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from redis_client.redis_client import redis_client



class ComparingDataKtc(APIView):
    def get(self, request):
        try:
            redis_data = redis_client.get_data_from_redis(name='ktc_wacom')
            if not redis_data:
                return Response(
                    {"error": "No data returned from database."},
                    status=status.HTTP_204_NO_CONTENT
                )
            data = json.loads(redis_data.decode("utf-8"))
            #serializer = ScrapedDataSerializer(data)

            return Response(data, status=status.HTTP_200_OK)

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
    def get(self, request, partner_name):
        try:
            raw_data = redis_client.get_data_from_redis(f"partner_data:{partner_name}")

            if not raw_data:
                return Response(
                    {"error": f"No data available for partner: {partner_name}."},
                    status=status.HTTP_404_NOT_FOUND
                )

            data = json.loads(raw_data.decode("utf-8"))
            return Response({"partner_name": partner_name, "data": data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": f"An unexpected error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )