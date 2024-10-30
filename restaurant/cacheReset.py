import os
from django.core.cache import cache

# Set DJANGO_SETTINGS_MODULE to your project's settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'restaurant.settings')  # Adjust if settings file name differs

# Clear the cache
cache.clear()
