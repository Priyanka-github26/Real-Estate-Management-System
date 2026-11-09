
from django.contrib import admin
from .models import (
    Agent,
    Property,
    PropertyImage,
    Client,
    PropertyInquiry,
    PropertyTour,
    FavoriteProperty,
    PropertyViewLog
)


class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 1


@admin.register(Agent)
class AgentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'experience', 'is_active')
    search_fields = ('name', 'email')
    list_filter = ('is_active',)


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'property_type', 'listing_type',
        'price', 'city', 'status', 'agent'
    )
    search_fields = ('title', 'city', 'address')
    list_filter = ('property_type', 'listing_type', 'status', 'city')
    inlines = [PropertyImageInline]


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'client_type')
    search_fields = ('name', 'email', 'phone')
    list_filter = ('client_type',)


@admin.register(PropertyInquiry)
class PropertyInquiryAdmin(admin.ModelAdmin):
    list_display = ('client', 'property', 'status', 'inquiry_date')
    search_fields = ('client__name', 'property__title')
    list_filter = ('status', 'inquiry_date')


@admin.register(PropertyTour)
class PropertyTourAdmin(admin.ModelAdmin):
    list_display = ('client', 'property', 'tour_date', 'tour_time', 'status')
    list_filter = ('status', 'tour_date')


@admin.register(FavoriteProperty)
class FavoritePropertyAdmin(admin.ModelAdmin):
    list_display = ('user', 'property', 'created_at')
    search_fields = ('user__username', 'property__title')


@admin.register(PropertyViewLog)
class PropertyViewLogAdmin(admin.ModelAdmin):
    list_display = ('property', 'user', 'viewed_at', 'ip_address')
    list_filter = ('viewed_at',)
    search_fields = ('property__title',)
