from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from cabrides.models import User, Ride

def index(request):
    latest_cab_rides = Ride.objects.order_by('-ride_date')[:5]
    context = {'latest_rides_list': latest_cab_rides}
    return render(request, 'cabrides/index.html', context)

def add_rider(request, ride_id, user_id):
    r = get_object_or_404(Ride, pk=ride_id)
    return HttpResponse("fuck you") 
