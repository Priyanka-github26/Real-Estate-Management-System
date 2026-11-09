from django.shortcuts import render, get_object_or_404

def home(request):
    return render(request, 'properties/home.html')

def property_list(request):
    from .models import Property

    properties = Property.objects.all()

    return render(
        request,
        'properties/property_list.html',
        {'properties': properties}
    )

def property_detail(request, property_id):
    from .models import Property

    property = get_object_or_404(Property, id=property_id)

    return render(
        request,
        'properties/property_detail.html',
        {'property': property}
    )