from rest_framework.decorators import api_view, throttle_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.throttling import AnonRateThrottle
from ..models import Product
from ..serializers import ProductSerializer, ContactRequestSerializer
import logging

logger = logging.getLogger('django')


class ContactRateThrottle(AnonRateThrottle):
    rate = '5/hour'


@api_view(['GET'])
def get_products(request) -> Response:
    """ 
    Endpoint to retrieve all products.
    Returns a list of products serialized in JSON format.
    If an error occurs during retrieval, it logs the error and returns a 500 status code.
    """
    try:
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    except Exception as e:
        logger.error(f"Error retrieving products: {e}")
        return Response({'message': 'Ошибка при получении продуктов.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@throttle_classes([ContactRateThrottle])
def send_contacts(request) -> Response:
    """
    Endpoint to send a contact request.
    Validates the request data and saves it if valid.
    Rate limited to 5 requests per hour per IP.
    """
    serializer = ContactRequestSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'success': True})
    return Response({'success': False, 'errors': serializer.errors}, status=400)
