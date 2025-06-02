from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..models import Products
from ..serializers import ProductSerializer, ContactRequestSerializer
import logging

logger = logging.getLogger(__name__)


@api_view(['GET'])
def get_products(request):
    try:
        products = Products.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    except Exception as e:
        logger.error(f"Error retrieving products: {e}")
        return Response({'message': 'Ошибка при получении продуктов.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def send_contacts(request):
    serializer = ContactRequestSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'success': True})
    return Response({'success': False, 'errors': serializer.errors}, status=400)
