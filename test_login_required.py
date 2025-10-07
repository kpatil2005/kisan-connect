#!/usr/bin/env python
"""
Simple test script to verify login requirements are working
Run this from the Django project directory: python test_login_required.py
"""

import os
import sys
import django
from django.conf import settings

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ec.settings')
django.setup()

from django.test import Client
from django.urls import reverse
from django.contrib.auth.models import User

def test_login_requirements():
    """Test that protected views require login"""
    client = Client()
    
    # Test URLs that should require login
    protected_urls = [
        '/schemes/',
        '/weather/',
        '/crops/',
        '/fertilizers/',
        '/marketplace/',
        '/forum/',
        '/news/',
        '/support/',
        '/prediction/',
        '/advice/',
    ]
    
    print("Testing login requirements...")
    print("=" * 50)
    
    # Test that protected URLs redirect to login
    for url in protected_urls:
        try:
            response = client.get(url, follow=False)
            if response.status_code == 302:  # Redirect
                print(f"✅ {url} - Correctly redirects (status: {response.status_code})")
            else:
                print(f"❌ {url} - Should redirect but got status: {response.status_code}")
        except Exception as e:
            print(f"⚠️  {url} - Error: {e}")
    
    # Test that home page is accessible
    try:
        response = client.get('/')
        if response.status_code == 200:
            print(f"✅ / (home) - Accessible without login (status: {response.status_code})")
        else:
            print(f"❌ / (home) - Should be accessible but got status: {response.status_code}")
    except Exception as e:
        print(f"⚠️  / (home) - Error: {e}")
    
    print("=" * 50)
    print("Test completed!")

if __name__ == "__main__":
    test_login_requirements()