from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from cabrides.models import CabUser, Ride

@login_required(login_url='/cabrides/login')
def index(request):
    latest_cab_rides = Ride.objects.order_by('-ride_date')[:5]
    context = {'latest_rides_list': latest_cab_rides}
    return render(request, 'cabrides/index.html', context)


def login_page(request):
    return render(request, 'cabrides/login.html', {})


def login_user(request):
    try:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/cabrides/')
        else:
            return HttpResponse("you don't belong!")
    except KeyError:
        return loggedin_index(request)


def logout_user(request):
    logout(request)
    return redirect('/cabrides/login/')


def add_rider(request, ride_id, user_id):
    ride = get_object_or_404(Ride, pk=ride_id)
    #user = get_object_or_404(CabUser, pk=user_id)
    return HttpResponse("ride: %s, user to be added: %s" % (ride, user_id)) 
