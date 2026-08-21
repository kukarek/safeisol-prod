from rest_framework.decorators import api_view, throttle_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.throttling import AnonRateThrottle
from ..models import Product, TrackerEvent
from ..serializers import ProductSerializer, ContactRequestSerializer
import logging
import urllib.request
import json

logger = logging.getLogger('django')


def resolve_geo(ip):
    """
    Определение геолокации по IP через бесплатное API ip-api.com
    (45 запросов/мин без ключа, работает из РФ).
    Возвращает dict с данными или пустой dict.
    """
    if not ip or ip in ('127.0.0.1', '::1'):
        return {}
    try:
        url = f'http://ip-api.com/json/{ip}?fields=status,country,countryCode,regionName,city,lat,lon,timezone'
        req = urllib.request.Request(url, headers={'User-Agent': 'SAFEISOL-Tracker/1.0'})
        with urllib.request.urlopen(req, timeout=3) as resp:
            data = json.loads(resp.read().decode())
            if data.get('status') == 'success':
                return {
                    'country': data.get('country', ''),
                    'country_code': data.get('countryCode', ''),
                    'city': data.get('city', ''),
                    'region': data.get('regionName', ''),
                    'latitude': data.get('lat'),
                    'longitude': data.get('lon'),
                    'timezone': data.get('timezone', ''),
                }
    except Exception as e:
        logger.debug(f"Geo lookup failed for {ip}: {e}")
    return {}


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


class TrackerRateThrottle(AnonRateThrottle):
    rate = '120/minute'


@api_view(['POST'])
@throttle_classes([TrackerRateThrottle])
def track_event(request) -> Response:
    """
    Endpoint для приёма событий трекера.
    Принимает JSON: { event_type, url, metadata?, product?, category? }
    visitor_id и session_id берутся из cookie, IP и User-Agent — из запроса.
    """
    try:
        data = request.data
        event_type = data.get('event_type')
        url = data.get('url', '')

        if not event_type or not url:
            return Response(
                {'success': False, 'message': 'event_type и url обязательны'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        valid_types = [t[0] for t in TrackerEvent.EVENT_TYPES]
        if event_type not in valid_types:
            return Response(
                {'success': False, 'message': f'Неизвестный event_type: {event_type}'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')

        # Geo lookup через ip-api.com
        geo_data = resolve_geo(ip)

        # Мержим geo_data в metadata
        metadata = data.get('metadata', {})
        if geo_data:
            metadata['geo'] = geo_data

        TrackerEvent.objects.create(
            event_type=event_type,
            url=url,
            product=data.get('product', ''),
            category=data.get('category', ''),
            metadata=metadata,
            ip_address=ip,
            user_agent=request.META.get('HTTP_USER_AGENT', ''),
            visitor_id=request.COOKIES.get('visitor_id', ''),
            session_id=request.COOKIES.get('session_id', ''),
        )

        return Response({'success': True})
    except Exception as e:
        logger.error(f"Tracker error: {e}")
        return Response(
            {'success': False, 'message': 'Внутренняя ошибка'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
