from django.shortcuts import render
import calendar
from calendar import HTMLCalendar
from datetime import datetime


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
