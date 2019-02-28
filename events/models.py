from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
import datetime


class Event(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    poster = models.ImageField(upload_to='event_posters')
    release_date = models.DateField()
    location = models.TextField()
    capacity = models.IntegerField()
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='events')
    
    
    
    class Meta:
        ordering = ['release_date', 'title', ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('event-detail', kwargs={'event_id': self.id})
    
    def tickets_available(self):
        tickets_booked = sum(self.bookings.all().values_list('number_of_tickets', flat=True))
        return self.capacity - tickets_booked
    
        


# def get_update_url(self):
 #   return reverse('event-update', kwargs={'event_id': self.id})
    

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='bookings')
    number_of_tickets = models.IntegerField(default=1)

    def __str__(self):
        return "%s booked by %s"%(self.event.title, self.user.username) 