from django.shortcuts import render, get_object_or_404, redirect
from .models import Property, Agent, Client, PropertyInquiry, PropertyTour
from .forms import ClientForm, PropertyInquiryForm

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

def client_register(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('property_list')

    else:
        form = ClientForm()

    return render(request, 'properties/client_register.html', {
        'form': form
    })
    
def property_inquiry(request, property_id):
    property = get_object_or_404(Property, id=property_id)

    if request.method == 'POST':
        form = PropertyInquiryForm(request.POST)

        if form.is_valid():
            inquiry = form.save(commit=False)

            # Find the registered client using their email
            email = request.POST.get('email', '').strip()
            client = Client.objects.filter(email__iexact=email).first()

            if client:
                inquiry.client = client
                inquiry.property = property
                inquiry.save()
                return redirect('property_detail', property_id=property.id)

            form.add_error(None, 'Please register as a client first.')

    else:
        form = PropertyInquiryForm()

    return render(request, 'properties/property_inquiry.html', {
        'form': form,
        'property': property,
    })
    
def dashboard(request):
    context = {
        'total_properties': Property.objects.count(),
        'available_properties': Property.objects.filter(status='available').count(),
        'sold_properties': Property.objects.filter(status='sold').count(),
        'rented_properties': Property.objects.filter(status='rented').count(),
        'total_agents': Agent.objects.count(),
        'total_clients': Client.objects.count(),
        'total_inquiries': PropertyInquiry.objects.count(),
        'pending_inquiries': PropertyInquiry.objects.filter(status='new').count(),
        'total_tours': PropertyTour.objects.count(),
    }

    return render(request, 'properties/dashboard.html', context)

