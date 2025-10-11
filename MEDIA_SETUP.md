# Fix Product Images Not Showing

## Quick Fix Steps:

### 1. Create media folder structure:
```
ec/
  media/
    product/
      seeds.jpg
      fertilizer.jpg
      machinery.jpg
      equipment.jpg
```

### 2. Run these commands in terminal:
```bash
cd Plant_Disease_Dataset\ec
mkdir media
mkdir media\product
```

### 3. Add placeholder images:
Download any 4 images and rename them as:
- seeds.jpg
- fertilizer.jpg  
- machinery.jpg
- equipment.jpg

Place them in: `ec/media/product/`

### 4. Verify settings.py has:
```python
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"
```

### 5. Verify ec/urls.py has:
```python
from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

### 6. In templates, use:
```html
<img src="{{ product.product_image.url }}" alt="{{ product.title }}">
```

OR with fallback:
```html
{% if product.product_image %}
    <img src="{{ product.product_image.url }}" alt="{{ product.title }}">
{% else %}
    <img src="{% static 'app/images/placeholder.jpg' %}" alt="{{ product.title }}">
{% endif %}
```

### 7. Restart Django server:
```bash
python manage.py runserver
```

Your images should now display!
