#!/usr/bin/env python
"""
Import products to production database
Run on Render Shell: python import_products.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ec.settings')
django.setup()

from django.core.management import call_command

try:
    call_command('loaddata', 'products_backup.json')
    print("✅ Products imported successfully!")
except Exception as e:
    print(f"❌ Error: {e}")
