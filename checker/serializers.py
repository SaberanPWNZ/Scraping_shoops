from rest_framework import serializers

from checker.models import PartnerItem


class PartnerScrapingInfoSerializer(serializers.Serializer):
    pass



class PartnerItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PartnerItem
        fields = ['article', 'availability', 'price', 'status', 'last_updated', 'partner']
