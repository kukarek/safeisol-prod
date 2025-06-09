# main/serializers.py
from rest_framework import serializers
from .models import Product, ContactRequest


class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer for Product model.
    Includes an additional 'url' field which returns the absolute URL for the product.
    """
    url = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'title', 'url']

    def get_url(self, obj) -> str:
        """
        Returns the absolute URL for the product using its slug.
        """
        return obj.get_absolute_url()


class ContactRequestSerializer(serializers.ModelSerializer):
    """
    Serializer for ContactRequest model.
    Serializes contact request fields needed for creating or listing contact requests.
    """
    class Meta:
        model = ContactRequest
        fields = ['name', 'phone', 'email', 'comment']
