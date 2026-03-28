"""FastAPI application for the biodynamics calendar."""

from fastapi import FastAPI
from fastapi.responses import PlainTextResponse

app = FastAPI()


@app.get("/biodynamics/calendar.ics", response_class=PlainTextResponse)
async def calendar():
    """Return biodynamics calendar in iCalendar format."""
    return "\r\n".join([
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//biodynamics//EN",
        "END:VCALENDAR",
    ])
