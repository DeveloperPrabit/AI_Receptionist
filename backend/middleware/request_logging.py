import logging
import time

logger = logging.getLogger(__name__)

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()
        
        response = self.get_response(request)
        
        duration = time.time() - start_time
        
        log_data = {
            'user': request.user.pk if request.user.is_authenticated else 'Anonymous',
            'remote_address': request.META.get('REMOTE_ADDR'),
            'server_hostname': request.META.get('SERVER_NAME'),
            'request_method': request.method,
            'request_path': request.path,
            'response_status': response.status_code,
            'response_time': duration,
            'user_agent': request.META.get('HTTP_USER_AGENT', '')
        }
        
        logger.info(msg="Request processed", extra=log_data)
        
        return response