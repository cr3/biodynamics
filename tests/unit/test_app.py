"""Unit tests for the app module."""

from datetime import date
from unittest.mock import patch

from fastapi.testclient import TestClient

from biodynamics.app import app

client = TestClient(app)


@patch("biodynamics.app.generate_calendar")
def test_calendar_default(mock_gen):
    """Endpoint returns text/calendar content type."""
    mock_gen.return_value.to_ical.return_value = b"BEGIN:VCALENDAR\r\nEND:VCALENDAR"
    response = client.get("/biodynamics/calendar.ics")
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/calendar; charset=utf-8"
    assert "BEGIN:VCALENDAR" in response.text


@patch("biodynamics.app.generate_calendar")
def test_calendar_custom_range(mock_gen):
    """Endpoint accepts start and end query params."""
    mock_gen.return_value.to_ical.return_value = b"BEGIN:VCALENDAR\r\nEND:VCALENDAR"
    response = client.get("/biodynamics/calendar.ics?start=2026-04-01&end=2026-05-01")
    assert response.status_code == 200
    mock_gen.assert_called_once_with(date(2026, 4, 1), date(2026, 5, 1))
