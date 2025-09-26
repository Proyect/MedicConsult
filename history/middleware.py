from django.core.cache import cache
from django.http import HttpResponseTooManyRequests
from django.conf import settings
import time

class RateLimitMiddleware:
    """
    Middleware para limitar el número de intentos de login por IP
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Solo aplicar rate limiting en login si está habilitado
        if (getattr(settings, 'RATE_LIMIT_ENABLE', False) and 
            request.path == '/login/' and 
            request.method == 'POST'):
            
            ip_address = self.get_client_ip(request)
            cache_key = f"rate_limit_{ip_address}"
            
            # Obtener intentos actuales
            attempts = cache.get(cache_key, 0)
            max_attempts = getattr(settings, 'RATE_LIMIT_ATTEMPTS', 5)
            window = getattr(settings, 'RATE_LIMIT_WINDOW', 300)
            
            if attempts >= max_attempts:
                return HttpResponseTooManyRequests(
                    "Demasiados intentos de login. Intenta nuevamente más tarde."
                )
            
            # Incrementar contador
            cache.set(cache_key, attempts + 1, window)
        
        response = self.get_response(request)
        return response
    
    def get_client_ip(self, request):
        """Obtener la IP real del cliente"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

