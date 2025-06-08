import logging
logger = logging.getLogger('django.request')


class CacheControlMiddleware:
    """
    Middleware to set Cache-Control headers for static files.
    This middleware sets a long cache duration for static files to improve performance.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response['Cache-Control'] = 'public, max-age=31536000'
        return response
    

class LogAllRequestsMiddleware:
    """
    Middleware to log all incoming requests.
    This middleware logs the HTTP method and full path of each request.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        logger.info(f"{request.method} {request.get_full_path()}")
        return self.get_response(request)