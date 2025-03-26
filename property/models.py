#
from django.db import models
from app.models import CustomUser
from django.utils.timezone import now

# Create your models here.


TYPE_CHOICES = [
    ('House', 'House'),
    ('Hostels', 'Hostels'),
    ('Hotel', 'Hotel'),
    ('Restaurant', 'Restaurant'),
]

class House(models.Model):
    name = models.CharField(max_length=50)
    mail = models.EmailField(default='', null=True, blank=True)
    phone = models.CharField(max_length=20, default="", null=True, blank=True)
    address = models.CharField(max_length=300, default="")
    location = models.CharField(max_length=200, default="")
    bedrooms = models.PositiveIntegerField(null=True, blank=True)
    bathrooms = models.PositiveIntegerField(null=True, blank=True)
    price = models.IntegerField(null=True, blank=True)
    is_available = models.BooleanField(default=True)
    type = models.CharField(
        max_length=20, 
        choices=TYPE_CHOICES, 
        default='House'  # Changed the default to a valid choice
    )
    description = models.TextField(max_length=1000)  # Increased the max_length for more flexibility
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, related_name='owned_houses')
    image = models.ImageField(upload_to='houses/', default='', blank=True)
    image2 = models.ImageField(upload_to='houses/', default='', blank=True)
    image3 = models.ImageField(upload_to='houses/', default='', blank=True)

    # Added blank=True for flexibility in form submissions

    def __str__(self):
        return self.name

class AppliedHouses(models.Model):
    house = models.ForeignKey(House, on_delete=models.CASCADE, related_name='applied_houses')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='applied_user')
    applied_date = models.DateField(auto_now_add=now())

    def __str__(self):
        return  f"{self.user.name}, applied on {self.applied_date}"