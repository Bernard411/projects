from django.db import models
from django.contrib.auth.models import User

class Item(models.Model):
    COLOR_CHOICES = [
        ('red', 'Red'),
        ('blue', 'Blue'),
        ('green', 'Green'),
        # Add more colors as needed
    ]

    CATEGORY_CHOICES = [
        ('shoes', 'Shoes'),
        ('t-shirts', 'T-Shirts'),
        ('pants', 'Pants'),
        # Add more categories as needed
    ]

    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    color = models.CharField(max_length=50, choices=COLOR_CHOICES)
    image_url = models.URLField()

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    preferred_colors = models.CharField(max_length=200)  # e.g., "red,blue,green"
    preferred_categories = models.CharField(max_length=200)  # e.g., "shoes,t-shirts"

    def __str__(self):
        return self.user.username
