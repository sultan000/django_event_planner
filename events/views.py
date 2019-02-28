from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views import View
from django.contrib import messages
from .forms import UserSignup, UserLogin, EventForm, BookingForm
from .models import Event, Booking
from django.db.models import Q
from django.http import JsonResponse
import datetime
import requests

def book(request, event_id):
    if request.user.is_anonymous:
        return redirect('Login')
    event_obj = Event.objects.get(id=event_id)
    reserve, created = Event.objects.get_or_create(user=request.user, event=event_obj)
    if created:
        booked = True
    else:
        booked = False
        reserve.delete()

    response = {
        "booked": booked,   
    }
    return JsonResponse(response)


def dashboard(request):
    user = request.user
    events = Event.objects.filter(organizer=user)
    # history_of_events = Booking.objects.filter(user=request.user).filter(event__release_date__lt=datetime.date.today())
    booking = Booking.objects.filter(user=user)
    attended_events = request.user.bookings.all()
    context = {
        'events': events,
        'attended_events': attended_events,
        # 'history_of_events': history_of_events,
        'booking': booking,
    }
    return render(request,'dashboard.html', context)

def home(request):
    return render(request, 'home.html')

def event_list(request):
    print(datetime.date.today())
    events = Event.objects.filter(release_date__gte=datetime.date.today())
    query = request.GET.get('Search')
    if query:
        events = events.filter(
            Q(title__icontains=query)|
            Q(description__icontains=query)|
            Q(organizer__username__icontains=query)
        ).distinct()
    context = {
        'events': events,
    }
    return render(request,'event_list.html', context)

def event_detail(request, event_id):
    event = Event.objects.get(id= event_id)
    tickets = event.bookings.all()
    if request.user.is_anonymous:
        return redirect('login')
    form_ticket = BookingForm()
    #if request.method == "POST":
        #form = BookingForm(request.POST)
        
        #if form.is_valid():
            #booking = form.save(commit=False)
            #booking.user = request.user
            #booking.event = event
            #booking.save()
       
    context = {
        'event': event,
        'form': form_ticket,
        'tickets': tickets
    }
    return render(request,'event_detail.html', context)


def add_event(request):
    if request.user.is_anonymous:
        return redirect('login')
    form = EventForm()
    if request.method == "POST":
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            print("VALID")
            event = form.save(commit=False)
            event.organizer = request.user
            form.save()
            return redirect('event-list')
        print("INVALID")
    context = {
        'form': form,
    }
    return render(request, 'add_event.html', context )
    


def add_ticket(request, event_id):
    event = Event.objects.get(id=event_id)
    total_tickets_available = event.tickets_available()
    form_ticket = BookingForm(request.POST)
    if form_ticket.is_valid():
        booking = form_ticket.save(commit=False)
        if total_tickets_available == 0:
            messages.success(request, "nothing")
            return redirect('event-detail' , event_id )
        elif booking.number_of_tickets > total_tickets_available or booking.number_of_tickets < 0 :
            messages.success(request, "Somthing went wrong")
            return redirect('event-detail' , event_id )
        else:
            booking.event = event
            booking.user = request.user
            booking.save()
            messages.success(request, "successfuly booked")
            return redirect('event-list')
    return redirect('event-detail',event_id)
      #  if tickets.tickets_available < 0 or tickets.number_of_tickets > event.tickets_available:
       #         messages.warning( "No seats available")
   



def update_event(request,event_id):
    event = Event.objects.get(id= event_id)

    if request.user.is_anonymous:
        return redirect('login')

    if not(request.user.is_staff or request.user == event.organizer):
        return redirect('login')
    form = EventForm(instance=event)
    if request.method == "POST":
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            print("VALID")
            form.save()
            return redirect(event)
        print(form.errors)
    context = {
        'form': form,
        "event": event,
    }
    return render(request, 'update_event.html', context)

def delete_event(request, event_id):

    if request.user.is_anonymous:
        return redirect('login')

    if not request.user.is_staff and not request.user == Event.objects.get(id= event_id).organizer:
        return redirect('event-list')

    Event.objects.get(id= event_id).delete()
    return redirect('event-list')



class Signup(View):
    form_class = UserSignup
    template_name = 'signup.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(user.password)
            user.save()
            messages.success(request, "You have successfully signed up.")
            login(request, user)
            return redirect("home")
        messages.warning(request, form.errors)
        return redirect("signup")


class Login(View):
    form_class = UserLogin
    template_name = 'login.html' 

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            auth_user = authenticate(username=username, password=password)
            if auth_user is not None:
                login(request, auth_user)
                
                if Event.objects.filter(organizer=auth_user).count() > 0:
                    messages.success(request, "Welcome Back!")
                    return redirect("dashboard")
                messages.success(request, "Welcome Back!")    
                return redirect('home')
            messages.warning(request, "Wrong email/password combination. Please try again.")
            return redirect("login")
        messages.warning(request, form.errors)
        return redirect("login")


class Logout(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        messages.success(request, "You have successfully logged out.")
        return redirect("login")

