from django.contrib import admin
from django.urls import path, include
from app import views
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.views.generic import TemplateView

handler404 = lambda request, exception: TemplateView.as_view(template_name='app/404.html')(request)
handler500 = lambda request: TemplateView.as_view(template_name='app/500.html')(request)

# Language switching must be OUTSIDE i18n_patterns
urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
]

# Add i18n patterns for all other URLs
urlpatterns += i18n_patterns(
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),
    path("category/<slug:val>/", views.CategoryView.as_view(), name="category"),
    path("", include("app.urls")),
    prefix_default_language=False,  # Don't add /en/ for English
)

# Static files
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
