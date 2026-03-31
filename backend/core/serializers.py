from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    """مسلسل بيانات المنتج"""
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'barcode', 'name', 'category', 'category_name',
            'purchase_price', 'selling_price', 'quantity',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
