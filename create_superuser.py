#!/usr/bin/env python
import os
import django
from django.contrib.auth.models import User

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ec.settings')
django.setup()

# Create superuser
username = 'root'
email = 'kpatil800083@gmail.com'
password = 'root1234'

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
    print(f'Superuser {username} created successfully!')
else:
    # Update existing user password
    user = User.objects.get(username=username)
    user.set_password(password)
    user.save()
    print(f'Password updated for existing superuser {username}!')