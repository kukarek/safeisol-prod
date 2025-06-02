# main/serializers.py
from rest_framework import serializers
from .models import Products, ContactRequest

class ProductSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = Products
        fields = ['id', 'title', 'url']

    def get_url(self, obj):
        return obj.get_absolute_url()


class ContactRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactRequest
        fields = ['name', 'phone', 'email', 'comment']