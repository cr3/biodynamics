"""Unit tests for the app module."""

from fastapi.testclient import TestClient

from biodynamics.app import app

client = TestClient(app)


def test_calendar():
    """Test the calendar endpoint returns valid iCalendar."""
    response = client.get("/biodynamics/calendar.ics")
    assert response.status_code == 200
    assert "BEGIN:VCALENDAR" in response.text
    assert "END:VCALENDAR" in response.text
