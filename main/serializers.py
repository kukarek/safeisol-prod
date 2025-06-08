# main/serializers.py
from rest_framework import serializers
from .models import Product, ContactRequest

class ProductSerializer(serializers.ModelSerializer):
    """Serializer for Products model."""
    url = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'title', 'url']

    def get_url(self, obj):
        return obj.get_absolute_url()


class ContactRequestSerializer(serializers.ModelSerializer):
    """Serializer for ContactRequest model."""
    class Meta:
        model = ContactRequest
        fields = ['name', 'phone', 'email', 'comment']