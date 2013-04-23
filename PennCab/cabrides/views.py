from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from cabrides.models import CabUser, Ride


def index(request):
    latest_cab_rides = Ride.objects.order_by('ride_date')
    user = request.user
    # NEED TO FILTER OUT RIDES IN PAST!
    if user.is_authenticated:
        latest_rides_tup = [(ride, ride.is_participant(user), ride.is_owner(user))
            for ride in latest_cab_rides]
    else:
        latest_rides_tup = [(ride, False, False) for ride in latest_cab_rides]
    context = {
        'latest_rides': latest_rides_tup, 
        'user': request.user
    }
    return render(request, 'cabrides/index.html', context)


@login_required(login_url='/cabrides/login')
def view_user(request):
    user = request.user
    latest_user_rides = Ride.objects.filter(
        participants__email=user.email).order_by('ride_date')
    latest_rides_tup = [(ride, True, ride.is_owner(user)) 
        for ride in latest_user_rides]
    context = {
        'latest_rides': latest_rides_tup,
        'user': request.user,
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
    return redirect('/cabrides/')


def signup(request):
    return render(request, 'cabrides/signup.html', {})


def signup_user(request):
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    phone_number = request.POST['phone_number']
    email = request.POST['email']
    password1 = request.POST['password1']
    if (first_name == '' or last_name == '' or phone_number == ''
        or email == '' or password1 == ''):
        return HttpResponse("Please fill in all the fields!")
    else:
        CabUser.objects.create_user(first_name.title(), last_name.title(),
            phone_number, email, password1)
        return redirect('/cabrides/')


def new_ride(request):
    context = {'user': request.user}
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


def search(request):
    term = request.POST['search-term']
    if term == '':
        return redirect('/cabrides/')
    return redirect('/cabrides/search/%s' % term)


def search_term(request, term):
    user = request.user
    search_rides = Ride.objects.filter(
        destination__contains=term).order_by('ride_date')
    if user.is_authenticated:
        rides_tup = [(ride, ride.is_participant(user), ride.is_owner(user)) 
            for ride in search_rides]
    else:
        rides_tup = [(ride, False, False) for ride in search_rides]
    context = {
        'latest_rides': rides_tup,
        'user': request.user,
    }
    return render(request, 'cabrides/index.html', context)
