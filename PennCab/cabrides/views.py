from django.http import HttpResponse
from django.shortcuts import render

from cabrides.models import User, Ride

def index(request):
    latest_cab_rides = Ride.objects.order_by('-ride_date')[:5]
    context = {'latest_rides_list': latest_cab_rides}
    return render(request, 'cabrides/index.html', context)
