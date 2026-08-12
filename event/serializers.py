from rest_framework import serializers
from .models import EventCategory, Event, EventMember, Vendor


class EventCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = EventCategory
        fields = ['id', 'name', 'code', 'priority', 'status']


class EventSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Event
        fields = [
            'id', 'name', 'category', 'category_name', 'description', 'venue',
            'start_date', 'end_date', 'location', 'points', 'max_attendees',
            'status', 'scheduled_status', 'budget', 'sponsors',
        ]


class EventMemberSerializer(serializers.ModelSerializer):
    event_name = serializers.CharField(source='event.name', read_only=True)

    class Meta:
        model = EventMember
        fields = ['id', 'event', 'event_name', 'name', 'email', 'role']


class VendorSerializer(serializers.ModelSerializer):
    event_name = serializers.CharField(source='event.name', read_only=True)

    class Meta:
        model = Vendor
        fields = ['id', 'name', 'service_type', 'contract_status', 'event', 'event_name']