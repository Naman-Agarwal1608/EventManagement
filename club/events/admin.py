from django.contrib import admin
from .models import Venue
from .models import MyClubUser
from .models import Event

admin.site.register([Venue, MyClubUser, Event])
