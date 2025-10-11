# Production Media Setup (Cloudinary)

## Step 1: Install Cloudinary
```bash
pip install cloudinary django-cloudinary-storage
pip freeze > requirements.txt
```

## Step 2: Add to INSTALLED_APPS in settings.py
```python
INSTALLED_APPS = [
    # ... other apps
    'cloudinary_storage',
    'cloudinary',
    'app',
]
```

## Step 3: Get Cloudinary Credentials
1. Sign up at https://cloudinary.com (Free tier: 25GB storage)
2. Go to Dashboard
3. Copy: Cloud Name, API Key, API Secret

## Step 4: Add to .env file
```
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret
```

## Step 5: Update settings.py (Already done)
Settings now automatically use Cloudinary in production (DEBUG=False)

## Step 6: Upload images to Cloudinary
```python
# In Django shell
python manage.py shell

from app.models import Product
from cloudinary.uploader import upload

# Upload and update products
products = Product.objects.all()
for product in products:
    if product.category == 'SD':
        result = upload('path/to/seeds.jpg', folder='product')
        product.product_image = result['public_id']
    # Repeat for FT, MC, EQ
    product.save()
```

## Alternative: Use Supabase Storage (Free 1GB)
```bash
pip install supabase
```

```python
# settings.py
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')
SUPABASE_BUCKET = 'products'
```

## Quick Fix for Now (Development):
1. Create folders:
```bash
mkdir media\product
```

2. Add 4 placeholder images:
- media/product/seeds.jpg
- media/product/fertilizer.jpg
- media/product/machinery.jpg
- media/product/equipment.jpg

3. Restart server:
```bash
python manage.py runserver
```

Images will now work in development!
