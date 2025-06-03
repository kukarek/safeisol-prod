from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..models import Products
from ..serializers import ProductSerializer, ContactRequestSerializer
import logging

logger = logging.getLogger('django')


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
    if request.session.get('contact_sent'):
        return Response({'success': False, 'error': 'Заявка уже отправлена.'}, status=429)

    serializer = ContactRequestSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        # Помечаем сессию, что заявка отправлена
        request.session['contact_sent'] = True
        request.session.modified = True
        return Response({'success': True})
    return Response({'success': False, 'errors': serializer.errors}, status=400)
