from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from cabrides.models import CabUser, Ride

@login_required(login_url='/cabrides/login')
def index(request):
    latest_cab_rides = Ride.objects.order_by('ride_date')
    user = request.user
    latest_rides_tup = [(ride, ride.is_participant(user), ride.is_owner(user)) 
        for ride in latest_cab_rides]
    context = {
        'latest_rides': latest_rides_tup, 
        'user_name': request.user.first_name
    }
    return render(request, 'cabrides/index.html', context)


def view_user(request):
    latest_user_rides = Ride.objects.filter(
        ride_owner=request.user).order_by('ride_date')
    latest_rides_tup = [(ride, True, True) for ride in latest_user_rides]
    context = {
        'latest_rides': latest_rides_tup,
        'user_name': request.user.first_name,
        'user_rides': True
    }
    return render(request, 'cabrides/index.html', context)


def login_page(request):
    return render(request, 'cabrides/login.html', {})


def login_user(request):
    if 'signup' in request.POST:
        return redirect('/cabrides/signup/')
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


def signup(request):
    return render(request, 'cabrides/signup.html', {})


def signup_user(request):
    return HttpResponse("Signup user!")


def new_ride(request):
    context = {'user_name': request.user.first_name}
    return render(request, 'cabrides/new_ride.html', context)


def create_ride(request):
    from datetime import datetime
    try:
        origin = request.POST['origin']
        destination = request.POST['destination']
        if origin == '' or destination == '':
            return HttpResponse("fill everything in!")
        else:
            date = request.POST['date']
            time = request.POST['time']
            datetime_string = ' '.join([date, time])
            max_riders = request.POST['max_riders']
            date_object = datetime.strptime(datetime_string, '%m/%d/%Y %I:%M %p')
            new_ride = Ride(origin=origin, destination=destination,
                ride_owner=request.user, max_riders=max_riders, ride_date=date_object)
            new_ride.save()
            new_ride.participants.add(request.user)
            return redirect('/cabrides/')
    except KeyError:
        return HttpResponse("Not all fields were filled out.") 


def add_rider(request, ride_id):
    ride = get_object_or_404(Ride, pk=ride_id)
    user = request.user
    if 'join' in request.POST:
        try:
            ride.participants.add(user)
            ride.save()
            return redirect('/cabrides/')
        except Error:
            return HttpResponse("Something went wrong trying to add user")
    else:
        if ride.is_owner(user):
            Ride.objects.get(pk=ride.id).delete()
            return redirect('/cabrides/')
        else:
            try:
                ride.participants.remove(user)
                ride.save()
                return redirect('/cabrides/')
            except Error:
                return HttpResponse("Something went wrong trying to remove user")
