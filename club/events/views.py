from django.http import HttpResponseBadRequest, HttpResponseRedirect, HttpResponse
from django.shortcuts import redirect, render
from django.contrib import messages
import calendar
from calendar import HTMLCalendar
from datetime import datetime

from .models import Event, Venue
from .forms import VenueForm, EventForm, EventFormAdmin
import csv
from django.core.paginator import Paginator  # for pagination and stuff

from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import A4


def home(request, year=datetime.now().year, month=datetime.now().strftime("%B")):
    name = "Naman"
    month = month.title()
    # Convert month to month number
    month_number = int(list(calendar.month_name).index(month))

    # Making calendar
    cal = HTMLCalendar().formatmonth(year, month_number)
    # Get current year
    now = datetime.now()
    current_year = now.year
    time = now.strftime("%I:%M %p")
    return render(
        request,
        "events/home.html",
        {
            "name": name,
            "year": year,
            "month": month,
            "month_number": month_number,
            "cal": cal,
            "current_year": current_year,
            "time": time,
        },
    )


def all_events(request):
    event_list = Event.objects.all().order_by('-event_date')
    return render(request, "events/event_list.html", {'event_list': event_list})


def list_venues(request):
    venue_list = Venue.objects.all().order_by('name')
    # Set up pagiantion
    pag = Paginator(Venue.objects.all().order_by('name'), 2)
    page = request.GET.get('page')
    venues = pag.get_page(page)
    return render(request, 'events/venues.html', {'venue_list': venue_list, 'venues': venues})


def show_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    return render(request, 'events/show_venue.html', {'venue': venue})


def search_venues(request):
    if request.method == 'POST':
        searched = request.POST['searched']
        venues = Venue.objects.filter(name__contains=searched)
        return render(request, "events/search_venues.html", {'searched': searched, 'venues': venues})
    else:
        return HttpResponseBadRequest("You should not try this...")


def update_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    form = VenueForm(request.POST or None, instance=venue)
    if form.is_valid():
        form.save()
        return redirect('list_venues')
    return render(request, "events/update_venue.html", {'venue': venue, 'form': form})


def update_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    if request.user.is_superuser:
        form = EventFormAdmin(request.POST or None, instance=event)
    else:
        form = EventForm(request.POST or None, instance=event)
    if form.is_valid():
        form.save()
        return redirect('list_events')
    return render(request, "events/update_event.html", {'event': event, 'form': form})


def delete_event(request, event_id):
    try:
        event = Event.objects.get(pk=event_id)
        if request.user == event.manager:
            event.delete()
            messages.success(request, "Event deleted !!!")
        else:
            messages.error(
                request, "You are not authorised to delete this event !!!")
    except Exception as e:
        messages.error(request, f"{e}")
    return redirect("list_events")


def delete_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    venue.delete()
    return redirect("list_venues")


def add_venue(request):
    submitted = False
    if request.method == "POST":
        form = VenueForm(request.POST)
        if form.is_valid():
            venue = form.save(commit=False)
            venue.owner = request.user.id
            venue.save()
            return HttpResponseRedirect('add_venue?submitted=True')
    else:
        form = VenueForm
        if 'submitted' in request.GET:
            submitted = True
    return render(request, 'events/add_venue.html', {'form': form, 'submitted': submitted})


def add_event(request):
    submitted = False
    if request.method == "POST":
        if request.user.is_superuser:
            form = EventFormAdmin(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('add_event?submitted=True')
        else:
            form = EventForm(request.POST)
            if form.is_valid():
                event = form.save(commit=False)
                event.manager = request.user
                event.save()
                return HttpResponseRedirect('add_event?submitted=True')
    else:
        if request.user.is_superuser:
            form = EventFormAdmin
        else:
            form = EventForm
        if 'submitted' in request.GET:
            submitted = True
    return render(request, 'events/add_event.html', {'form': form, 'submitted': submitted})


def venue_txt(request):
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=venues.txt'

    venues = Venue.objects.all()
    for venue in venues:
        response.write(venue.name + '\n')
        response.write(venue.address + '\n')
        response.write(venue.zip_code + '\n')
        response.write(venue.phone + '\n')
        response.write(venue.web + '\n')
        response.write(venue.email_address + '\n')
        response.write("\n\n")

    return response


def venue_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=venues.csv'

    # Create a csv writer
    writer = csv.writer(response)

    # Model
    venues = Venue.objects.all()

    # Column Names
    writer.writerow(['Venue Name', 'Addrtess', 'Zip Code',
                    'Phone', 'Web Addresss', 'Email'])

    # Adding data
    for venue in venues:
        writer.writerow([venue.name, venue.address, venue.zip_code,
                        venue.phone, venue.web, venue.email_address])

    return response


def venue_pdf(request):

    venues = Venue.objects.all()
    # Create a byte stream buffer
    buf = io.BytesIO()
    # canvas
    canv = canvas.Canvas(buf, pagesize=A4, bottomup=0)
    textObj = canv.beginText()
    textObj.setTextOrigin(inch, inch)
    textObj.setFont("Helvetica", 14)

    for venue in venues:
        textObj.textLine(venue.name)
        textObj.textLine(venue.zip_code)
        textObj.textLine(venue.address)
        textObj.textLine(venue.phone)
        textObj.textLine(venue.web)
        textObj.textLine(venue.email_address)
        textObj.textLine("")

    canv.drawText(textObj)
    canv.showPage()
    canv.save()
    buf.seek(0)

    return FileResponse(buf, as_attachment=False, filename='venues.pdf')
