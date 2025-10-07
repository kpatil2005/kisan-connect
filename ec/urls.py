from django.contrib import admin
from django.urls import path, include
from app import views
from django.conf import settings
from django.conf.urls.static import static  

urlpatterns = [
    path("admin/", admin.site.urls),

    # ✅ keep home page here
    path("", views.home, name="home"),

    # ✅ keep category route
    path("category/<slug:val>/", views.CategoryView.as_view(), name="category"),

    # ✅ include rest of app urls
    path("", include("app.urls")),
]

# ✅ serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
