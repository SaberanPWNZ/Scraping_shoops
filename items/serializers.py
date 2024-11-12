from rest_framework import serializers
from .models import Item, Warranty, Category, Status

class ItemCreateSerializer(serializers.ModelSerializer):
    title = serializers.CharField(required=True)
    article = serializers.CharField(required=True)
    status = serializers.PrimaryKeyRelatedField(queryset=Status.objects.all(), required=True)
    image = serializers.ImageField(required=True)
    partner_price = serializers.DecimalField(max_digits=10, decimal_places=2, required=True)
    rrp_price = serializers.DecimalField(max_digits=10, decimal_places=2, required=True)
    warranty = serializers.PrimaryKeyRelatedField(queryset=Warranty.objects.all(), required=True)
    ean = serializers.CharField(max_length=50, required=False, allow_blank=True)
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), required=True)

    class Meta:
        model = Item
        fields = (
            'title',
            'article',
            'status',
            'image',
            'partner_price',
            'rrp_price',
            'warranty',
            'ean',
            'category'
        )

    def create(self, validated_data):
        item = Item(**validated_data)
        item.save()
        return item