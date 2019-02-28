from django.shortcuts import render
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    RetrieveUpdateAPIView,
    DestroyAPIView,
    CreateAPIView,
)
from events.models import Event
from .serializers import(
    EventDetailSerializer,
    EventListSerializer,
    EventCreateUpdateSerializer,
)
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from .permissions import Checking

class EventList(ListAPIView):
    queryset = Event.objects.all()
    serializer_class = EventListSerializer
    permission_classes = [AllowAny,]

class EventDetail(RetrieveAPIView):
    queryset = Event.objects.all()
    serializer_class = EventDetailSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'event_id'
    permission_classes = [AllowAny,]

class EventCreate(CreateAPIView):
    serializer_class = EventCreateUpdateSerializer
    permission_classes = [IsAuthenticated,]

    def perform_create(self, serializer):
        serializer.save(organizer=self.request.user)

class EventUpdate(RetrieveUpdateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventCreateUpdateSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'event_id'
    permission_classes = [Checking,]

class EventDelete(DestroyAPIView):
    queryset = Event.objects.all()
    lookup_field = 'id'
    lookup_url_kwarg = 'event_id'
    permission_classes = [Checking,]
