from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
import logging

logger = logging.getLogger(__name__)

class LoginRequiredMiddleware:
    """
    Middleware to enforce login for all views except public ones
    """
    def __init__(self, get_response):
        self.get_response = get_response
        self.public_urls = [
            '/',
            '/accounts/login/',
            '/signin/',
            '/registration/',
            '/password-reset/',
            '/password-reset/done/',
            '/password-reset-confirm/',
            '/password-reset-complete/',
            '/admin/',
        ]

    def __call__(self, request):
        try:
            if not request.user.is_authenticated:
                if not any(request.path.startswith(url) for url in self.public_urls):
                    request.session['next'] = request.get_full_path()
                    messages.info(request, "Please login to access this feature.")
                    return redirect('app:signin')
            
            response = self.get_response(request)
            return response
        except Exception as e:
            logger.error(f"Middleware error: {e}")
            return self.get_response(request)

class ErrorHandlerMiddleware:
    """Global error handler middleware"""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_exception(self, request, exception):
        logger.error(f"Unhandled exception: {exception}", exc_info=True)
        return render(request, 'app/error.html', {'error': 'An unexpected error occurred'}, status=500)