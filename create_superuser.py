#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ec.settings')
django.setup()

from django.contrib.auth.models import User

# Create superuser
username = 'root'
email = 'kpatil800083@gmail.com'
password = 'root1234'

try:
    if not User.objects.filter(username=username).exists():
        user = User.objects.create_superuser(username, email, password)
        user.is_staff = True
        user.is_active = True
        user.save()
        print(f'Superuser {username} created successfully!')
    else:
        # Update existing user password and ensure staff status
        user = User.objects.get(username=username)
        user.set_password(password)
        user.is_staff = True
        user.is_active = True
        user.is_superuser = True
        user.save()
        print(f'Password updated for existing superuser {username}!')
except Exception as e:
    print(f'Error creating superuser: {e}')