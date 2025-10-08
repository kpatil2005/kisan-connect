# Cloudinary Setup for Product Images

## Why Cloudinary?
Render's free tier has an ephemeral filesystem - uploaded files are deleted on server restart. Cloudinary provides permanent cloud storage for images.

## Setup Steps

### 1. Create Cloudinary Account
1. Go to https://cloudinary.com/users/register_free
2. Sign up for a **FREE account**
3. After login, go to Dashboard

### 2. Get Your Credentials
From the Cloudinary Dashboard, copy:
- **Cloud Name** (e.g., `dxxxxx`)
- **API Key** (e.g., `123456789012345`)
- **API Secret** (e.g., `abcdefghijklmnopqrstuvwxyz`)

### 3. Add to Render Environment Variables
1. Go to https://dashboard.render.com
2. Select your **kisan-connect** service
3. Go to **Environment** tab
4. Add these variables:

```
CLOUDINARY_CLOUD_NAME = your_cloud_name
CLOUDINARY_API_KEY = your_api_key
CLOUDINARY_API_SECRET = your_api_secret
```

5. Click **Save Changes**
6. Render will automatically redeploy

### 4. Test It
1. Go to https://kisan-connect.onrender.com/admin/
2. Login with `root` / `root1234`
3. Add a new product with an image
4. The image will now be stored on Cloudinary permanently!

## Benefits
✅ Images persist forever (even after server restarts)
✅ Fast CDN delivery worldwide
✅ Free tier: 25GB storage + 25GB bandwidth/month
✅ Automatic image optimization
✅ All users see the same images

## Verification
After setup, product images will have URLs like:
```
https://res.cloudinary.com/your_cloud_name/image/upload/v1234567890/product/image.jpg
```

Instead of:
```
/media/product/image.jpg (404 error)
```
