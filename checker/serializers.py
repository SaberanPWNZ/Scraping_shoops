from rest_framework import serializers
from .models import ScrapedData, ScrapedItem, Partner

class ScrapedItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScrapedItem
        fields = ['id', 'name', 'price', 'status']

class ScrapedDataSerializer(serializers.ModelSerializer):
    partner = serializers.CharField(source='partner.name')
    items = ScrapedItemSerializer(many=True)
    class Meta:
        model = ScrapedData
        fields = ['partner', 'created_at', 'last_update', 'items']
