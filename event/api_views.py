from rest_framework import generics, permissions
from .models import EventCategory, Event, EventMember, Vendor
from .serializers import (
    EventCategorySerializer, EventSerializer, EventMemberSerializer, VendorSerializer
)


class CategoryListAPI(generics.ListAPIView):
    queryset = EventCategory.objects.all()
    serializer_class = EventCategorySerializer
    permission_classes = [permissions.IsAuthenticated]


class EventListAPI(generics.ListAPIView):
    queryset = Event.objects.all().order_by('-id')
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated]


class EventDetailAPI(generics.RetrieveAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated]


class MemberListAPI(generics.ListAPIView):
    serializer_class = EventMemberSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = EventMember.objects.all()
        event_id = self.request.query_params.get('event')
        if event_id:
            qs = qs.filter(event_id=event_id)
        return qs


class VendorListAPI(generics.ListAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    permission_classes = [permissions.IsAuthenticated]