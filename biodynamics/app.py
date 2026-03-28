"""FastAPI application for the biodynamics calendar."""

from datetime import date, timedelta

from fastapi import FastAPI, Query
from fastapi.responses import Response

from biodynamics.calendar import generate_calendar

app = FastAPI()

_DEFAULT_DAYS = 90


@app.get("/biodynamics/calendar.ics")
async def calendar(
    start: date = Query(default=None, description="Start date (YYYY-MM-DD), defaults to today."),
    end: date = Query(default=None, description="End date (YYYY-MM-DD), defaults to start + 90 days."),
):
    """Return biodynamics planting calendar in iCalendar format."""
    if start is None:
        start = date.today()
    if end is None:
        end = start + timedelta(days=_DEFAULT_DAYS)

    cal = generate_calendar(start, end)
    return Response(
        content=cal.to_ical(),
        media_type="text/calendar",
    )
