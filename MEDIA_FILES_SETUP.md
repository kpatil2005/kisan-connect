# Fix Product Images on Hosted Site

## Problem
Product images show 404 error because Render doesn't persist uploaded files.

## Solution: Use Cloudinary (Free Cloud Storage)

### Step 1: Create Cloudinary Account
1. Go to https://cloudinary.com/users/register_free
2. Sign up (free tier: 25GB storage)
3. Get your credentials from Dashboard:
   - Cloud Name
   - API Key
   - API Secret

### Step 2: Install Cloudinary
```bash
pip install cloudinary django-cloudinary-storage
```

### Step 3: Update requirements.txt
Add these lines:
```
cloudinary==1.41.0
django-cloudinary-storage==0.3.0
```

### Step 4: Update settings.py
Add to INSTALLED_APPS (before 'django.contrib.staticfiles'):
```python
INSTALLED_APPS = [
    # ...
    'cloudinary_storage',
    'cloudinary',
    'django.contrib.staticfiles',
    # ...
]
```

Add Cloudinary config:
```python
import cloudinary

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.environ.get('CLOUDINARY_CLOUD_NAME'),
    'API_KEY': os.environ.get('CLOUDINARY_API_KEY'),
    'API_SECRET': os.environ.get('CLOUDINARY_API_SECRET')
}

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
```

### Step 5: Add Environment Variables on Render
In Render Dashboard → Environment:
```
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret
```

### Step 6: Upload Existing Images
Run locally:
```bash
python manage.py collectstatic
```

Then re-upload products via admin panel on hosted site with images.

## Alternative: Add Products Directly on Hosted Site
1. Go to https://kisan-connect.onrender.com/admin/
2. Add products with images directly there
3. Images will be stored in Cloudinary automatically
