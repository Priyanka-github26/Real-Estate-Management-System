
from django.shortcuts import render, get_object_or_404
from .models import Property


def home(request):
    return render(request, 'properties/home.html')


def property_list(request):
    city = request.GET.get('city')
    property_type = request.GET.get('property_type')
    listing_type = request.GET.get('listing_type')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    properties = Property.objects.all()

    # Search by city
    if city:
        properties = properties.filter(city__icontains=city)

    # Filter by property type
    if property_type:
        properties = properties.filter(property_type=property_type)

    # Filter by sale or rent
    if listing_type:
        properties = properties.filter(listing_type=listing_type)

    # Filter by minimum price
    if min_price:
        properties = properties.filter(price__gte=min_price)

    # Filter by maximum price
    if max_price:
        properties = properties.filter(price__lte=max_price)


    return render(
        request,
        'properties/property_list.html',
        {
            'properties': properties,
            'city': city,
            'property_type': property_type,
            'listing_type': listing_type,
            'min_price': min_price,
            'max_price': max_price,
        }
    )


def property_detail(request, property_id):
    property = get_object_or_404(Property, id=property_id)

    return render(
        request,
        'properties/property_detail.html',
        {'property': property}
    )
