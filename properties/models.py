
from django.db import models


class Agent(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    experience = models.PositiveIntegerField(default=0)
    profile_image = models.ImageField(
        upload_to='agents/',
        blank=True,
        null=True
    )
    bio = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Property(models.Model):

    PROPERTY_TYPES = [
        ('apartment', 'Apartment'),
        ('house', 'House'),
        ('villa', 'Villa'),
        ('commercial', 'Commercial'),
        ('land', 'Land'),
    ]

    LISTING_TYPES = [
        ('sale', 'For Sale'),
        ('rent', 'For Rent'),
    ]

    STATUS_CHOICES = [
        ('available', 'Available'),
        ('sold', 'Sold'),
        ('rented', 'Rented'),
        ('pending', 'Pending'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    property_type = models.CharField(
        max_length=20,
        choices=PROPERTY_TYPES
    )
    listing_type = models.CharField(
        max_length=10,
        choices=LISTING_TYPES
    )
    price = models.DecimalField(max_digits=12, decimal_places=2)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    bedrooms = models.PositiveIntegerField(default=0)
    bathrooms = models.PositiveIntegerField(default=0)
    area_sqft = models.PositiveIntegerField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='available'
    )
    
    
    latitude = models.DecimalField(
        max_digits=10,
        decimal_places=7,
        null=True,
        blank=True
    )

    longitude = models.DecimalField(
        max_digits=10,
        decimal_places=7,
        null=True,
        blank=True
    )


    agent = models.ForeignKey(
        Agent,
        on_delete=models.CASCADE,
        related_name='properties'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class PropertyImage(models.Model):

    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name='images'
    )

    image = models.ImageField(upload_to='properties/')

    caption = models.CharField(
        max_length=200,
        blank=True
    )

    is_primary = models.BooleanField(default=False)

    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.property.title}"


class Client(models.Model):

    CLIENT_TYPES = [
        ('buyer', 'Buyer'),
        ('seller', 'Seller'),
        ('tenant', 'Tenant'),
    ]

    name = models.CharField(max_length=100)

    email = models.EmailField(unique=True)

    phone = models.CharField(max_length=15)

    client_type = models.CharField(
        max_length=10,
        choices=CLIENT_TYPES,
        default='buyer'
    )

    address = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class PropertyInquiry(models.Model):

    INQUIRY_STATUS = [
        ('new', 'New'),
        ('contacted', 'Contacted'),
        ('in_progress', 'In Progress'),
        ('closed', 'Closed'),
    ]

    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name='inquiries'
    )

    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name='inquiries'
    )

    message = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=INQUIRY_STATUS,
        default='new'
    )

    inquiry_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.client.name} - {self.property.title}"


class PropertyTour(models.Model):

    TOUR_STATUS = [
        ('scheduled', 'Scheduled'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name='tours'
    )

    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name='tours'
    )

    tour_date = models.DateField()

    tour_time = models.TimeField()

    status = models.CharField(
        max_length=20,
        choices=TOUR_STATUS,
        default='scheduled'
    )

    notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Tour: {self.property.title} - {self.client.name}"


class FavoriteProperty(models.Model):

    user = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE,
        related_name='favorite_properties'
    )

    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name='favorited_by'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'property')

    def __str__(self):
        return f"{self.user.username} - {self.property.title}"


class PropertyViewLog(models.Model):

    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name='view_logs'
    )

    user = models.ForeignKey(
        'auth.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='property_views'
    )

    viewed_at = models.DateTimeField(auto_now_add=True)

    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.property.title} viewed at {self.viewed_at}"
