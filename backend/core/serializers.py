from rest_framework import serializers
from .models import Product, Supplier, Customer

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


class SupplierSerializer(serializers.ModelSerializer):
    """مسلسل بيانات المورد"""
    class Meta:
        model = Supplier
        fields = [
            'id', 'name', 'phone', 'balance', 'address',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class CustomerSerializer(serializers.ModelSerializer):
    """مسلسل بيانات العميل"""
    class Meta:
        model = Customer
        fields = [
            'id', 'name', 'phone', 'debt', 'address',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
