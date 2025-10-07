#!/usr/bin/env python
"""
Export products from local database to JSON file
Run: python export_products.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ec.settings_local')
django.setup()

from django.core import serializers
from app.models import Product

# Export all products
products = Product.objects.all()
data = serializers.serialize('json', products, indent=2)

with open('products_backup.json', 'w') as f:
    f.write(data)

print(f"✅ Exported {products.count()} products to products_backup.json")
print("📤 Upload this file to your repo and load it on Render")
