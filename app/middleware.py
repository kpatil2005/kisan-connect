from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages

class LoginRequiredMiddleware:
    """
    Middleware to enforce login for all views except public ones
    """
    def __init__(self, get_response):
        self.get_response = get_response
        # Define public URLs that don't require login
        self.public_urls = [
            '/',  # home page
            '/accounts/login/',  # login page
            '/signin/',  # custom signin page
            '/registration/',  # registration page
            '/password-reset/',  # password reset
            '/password-reset/done/',
            '/password-reset-confirm/',
            '/password-reset-complete/',
            '/admin/',  # admin (has its own auth)
        ]

    def __call__(self, request):
        # Check if user is authenticated or accessing public URL
        if not request.user.is_authenticated:
            # Allow access to public URLs
            if not any(request.path.startswith(url) for url in self.public_urls):
                # Store the current URL to redirect after login
                request.session['next'] = request.get_full_path()
                messages.info(request, "Please login to access this feature.")
                return redirect('app:signin')
        
        response = self.get_response(request)
        return response