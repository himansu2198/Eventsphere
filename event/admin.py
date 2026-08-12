from django.contrib import admin
from .models import EventCategory, Event, EventUserWish, EventMember, UserMark


@admin.register(EventCategory)
class EventCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'priority', 'status')
    list_filter = ('status',)
    search_fields = ('name', 'code')


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'status', 'start_date', 'end_date')
    list_filter = ('status', 'category')
    search_fields = ('name', 'venue')


@admin.register(EventUserWish)
class EventUserWishAdmin(admin.ModelAdmin):
    list_display = ('event', 'user', 'status')
    list_filter = ('status',)


@admin.register(EventMember)
class EventMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'event', 'role', 'email')
    list_filter = ('role', 'event')


@admin.register(UserMark)
class UserMarkAdmin(admin.ModelAdmin):
    list_display = ('member', 'status', 'marked_at')
    list_filter = ('status',)