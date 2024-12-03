from rest_framework import serializers
from .models import ScrapedData, ScrapedItem

class ScrapedItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScrapedItem
        fields = ('name', 'article', 'price', 'status')

class ScrapedDataSerializer(serializers.ModelSerializer):
    items = ScrapedItemSerializer(many=True)

    class Meta:
        model = ScrapedData
        fields = ('partner', 'created_at', 'last_update', 'items')
