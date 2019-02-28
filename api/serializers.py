from rest_framework import serializers
from events.models import Event


class EventListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'title',]

class EventDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'

class EventCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        exclude = ['organizer',]