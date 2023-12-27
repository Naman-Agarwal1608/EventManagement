from django.contrib import admin
from django.contrib.auth.models import Group
from .models import Venue
from .models import MyClubUser
from .models import Event

admin.site.register(MyClubUser)

admin.site.unregister(Group)


@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    '''Admin View for Venue'''

    list_display = ('name', 'address', 'phone')
    # list_filter = ('',)
    # raw_id_fields = ('',)
    # readonly_fields = ('',)
    search_fields = ('name', 'address')
    # date_hierarchy = ''
    ordering = ('name',)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    '''Admin View for Event'''

    fields = (('name', 'venue'), 'event_date',
              'description', 'manager', 'approved')
    list_display = ('name', 'event_date', 'venue')
    list_filter = ('event_date', 'venue')
    # raw_id_fields = ('',)
    # readonly_fields = ('',)
    # search_fields = ('',)
    # date_hierarchy = ''
    ordering = ('event_date',)
