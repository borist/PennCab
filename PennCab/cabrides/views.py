from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from cabrides.models import CabUser, Ride


def index(request):
    """
    The index/home page, displays all cab rides that are in the future in order of
    increases date/time of occurence.
    """
    latest_cab_rides = Ride.objects.order_by('ride_date')
    user = request.user
    if user.is_authenticated:
        latest_rides_tup = [(ride, ride.is_participant(user), ride.is_owner(user))
            for ride in latest_cab_rides if not ride.ride_in_past()]
    else:
        latest_rides_tup = [(ride, False, False) for ride in latest_cab_rides]
    context = {
        'latest_rides': latest_rides_tup, 
        'user': request.user
    }
    return render(request, 'cabrides/index.html', context)


@login_required(login_url='/cabrides/login')
def view_user(request):
    """
    Filter out and view only cab rides that the currently logged in
    user is a participant (or owner) of. Require log in, otherwise
    redirect to login page.
    """
    user = request.user
    latest_user_rides = Ride.objects.filter(
        participants__email=user.email).order_by('ride_date')
    latest_rides_tup = [(ride, True, ride.is_owner(user)) 
        for ride in latest_user_rides if not ride.ride_in_past()]
    context = {
        'latest_rides': latest_rides_tup,
        'user': request.user,
        'user_rides': True
    }
    return render(request, 'cabrides/index.html', context)


def login_page(request):
    """
    Render the login page for the app.
    """
    return render(request, 'cabrides/login.html', {})


def login_user(request):
    """
    Try to authenticate the user, and if successful log him in and redirect to
    the index page. If unsuccessful, return error page.
    """
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
    """
    Log out the currently logged in user and return to the index page.
    """
    logout(request)
    return redirect('/cabrides/')


def signup(request):
    """
    Render the signup page for the app.
    """
    return render(request, 'cabrides/signup.html', {})


def signup_user(request):
    """
    Try to sign up a user for an account. If any of the fields are blank or an error
    occurs, redirect to an error page. If successful, log the user in and redirect
    to the index page.
    """
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
        user = authenticate(username=email, password=password1)
        login(request, user)
        return redirect('/cabrides/')


def new_ride(request):
    """
    Render the page to create a new cab ride.
    """
    context = {'user': request.user}
    return render(request, 'cabrides/new_ride.html', context)


def create_ride(request):
    """
    Attempt to create a new cab ride from the request. If an error occurs
    (such as some fields not being filled out), return an error page.
    Otherwise if the creation is successful, redirect back to the index page.
    """
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
    """
    Attempt to add the logged in user to the ride with the given <ride_id>. If an
    error occurs, redirect to an error page. If successful, redirect back to index.
    """
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
    """
    Get search term from request. If it is not negative, perform the search.
    """
    term = request.POST['search-term']
    if term == '':
        return redirect('/cabrides/')
    return redirect('/cabrides/search/%s' % term)


def search_term(request, term):
    """
    (very) basic search by filtering destinations that contain the given term. Render
    filtered list.
    """
    user = request.user
    search_rides = Ride.objects.filter(
        destination__contains=term).order_by('ride_date')
    if user.is_authenticated:
        rides_tup = [(ride, ride.is_participant(user), ride.is_owner(user)) 
            for ride in search_rides if not ride.ride_in_past()]
    else:
        rides_tup = [(ride, False, False) for ride in search_rides]
    context = {
        'latest_rides': rides_tup,
        'user': request.user,
    }
    return render(request, 'cabrides/index.html', context)
