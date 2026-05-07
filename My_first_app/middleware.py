import time
import logging
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger('django.request')

class HTTPRequestLoggingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.start_time = time.time()
        
    def process_response(self, request, response):
        if hasattr(request, 'start_time'):
            response_time = (time.time() - request.start_time) * 1000
        else:
            response_time = 0
            
        logger.info(
            f"{request.method} {request.get_full_path()} {response.status_code} {response_time:.2f}ms",
            extra={
                'method': request.method,
                'path': request.get_full_path(),
                'status': response.status_code,
                'response_time': response_time,
            }
        )
        return response
