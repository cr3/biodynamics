"""FastAPI application for the biodynamics calendar."""

import argparse
from datetime import date, timedelta

from fastapi import FastAPI, Query
from fastapi.responses import Response

from biodynamics.calendar import generate_calendar

app = FastAPI(title="Biodynamics", docs_url="/biodynamics/docs")

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


def main():
    """Entry point for the biodynamics web server."""
    import uvicorn

    parser = argparse.ArgumentParser(
        description="Biodynamics web server",
    )
    parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="bind address (default: 127.0.0.1)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="port (default: 8000)",
    )
    parser.add_argument(
        "--reload",
        action="store_true",
        help="auto-reload",
    )
    args = parser.parse_args()
    uvicorn.run("biodynamics.app:app", host=args.host, port=args.port, reload=args.reload)
