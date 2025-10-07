#!/usr/bin/env python
import os
import sys
import django

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ec.settings')
django.setup()

# Test Gemini API
try:
    import google.generativeai as genai
    from django.conf import settings
    
    print("Testing Gemini API...")
    print(f"API Key exists: {bool(settings.GEMINI_API_KEY)}")
    print(f"API Key starts with: {settings.GEMINI_API_KEY[:10]}...")
    
    genai.configure(api_key=settings.GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")
    
    response = model.generate_content("What is farming?")
    print(f"Response: {response.text[:100]}...")
    print("✅ Gemini API working!")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Run: pip install google-generativeai")
except Exception as e:
    print(f"❌ API error: {e}")