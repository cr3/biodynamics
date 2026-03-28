"""Unit tests for the calendar module."""

from datetime import date
from unittest.mock import patch

from biodynamics.calendar import (
    CONSTELLATION_PLANT_TYPE,
    PlantType,
    generate_calendar,
    plant_type,
)
from biodynamics.moon import Constellation


def test_constellation_plant_type_complete():
    """Every constellation maps to a plant type."""
    for c in Constellation:
        assert c in CONSTELLATION_PLANT_TYPE


def test_plant_type_returns_valid_type():
    """plant_type returns one of the four plant types."""
    valid = {PlantType.FRUIT, PlantType.ROOT, PlantType.FLOWER, PlantType.LEAF}
    result = plant_type(date(2026, 3, 28))
    assert result in valid


@patch("biodynamics.calendar.moon_constellation", return_value=Constellation.ARIES)
def test_plant_type_fruit(mock_moon):
    """Aries (Fire) maps to Fruit."""
    result = plant_type(date(2026, 1, 1))
    assert result == PlantType.FRUIT
    assert result == "🍎"


@patch("biodynamics.calendar.moon_constellation", return_value=Constellation.TAURUS)
def test_plant_type_root(mock_moon):
    """Taurus (Earth) maps to Root."""
    result = plant_type(date(2026, 1, 1))
    assert result == PlantType.ROOT
    assert result == "🥕"


@patch("biodynamics.calendar.moon_constellation", return_value=Constellation.GEMINI)
def test_plant_type_flower(mock_moon):
    """Gemini (Air) maps to Flower."""
    result = plant_type(date(2026, 1, 1))
    assert result == PlantType.FLOWER
    assert result == "🌸"


@patch("biodynamics.calendar.moon_constellation", return_value=Constellation.CANCER)
def test_plant_type_leaf(mock_moon):
    """Cancer (Water) maps to Leaf."""
    result = plant_type(date(2026, 1, 1))
    assert result == PlantType.LEAF
    assert result == "🌿"


@patch("biodynamics.calendar.plant_type", return_value=PlantType.FRUIT)
def test_generate_calendar_structure(mock_plant_type):
    """Generated calendar has correct structure."""
    start = date(2026, 4, 1)
    end = date(2026, 4, 4)
    cal = generate_calendar(start, end)

    ical = cal.to_ical().decode()
    assert "BEGIN:VCALENDAR" in ical
    assert "END:VCALENDAR" in ical
    assert ical.count("BEGIN:VEVENT") == 3


@patch("biodynamics.calendar.plant_type", return_value=PlantType.ROOT)
def test_generate_calendar_event_summary(mock_plant_type):
    """Events use the plant type as summary."""
    cal = generate_calendar(date(2026, 4, 1), date(2026, 4, 2))
    ical = cal.to_ical().decode()
    assert "🥕" in ical


@patch("biodynamics.calendar.plant_type", return_value=PlantType.LEAF)
def test_generate_calendar_empty_range(mock_plant_type):
    """Empty range produces no events."""
    d = date(2026, 4, 1)
    cal = generate_calendar(d, d)
    ical = cal.to_ical().decode()
    assert "BEGIN:VEVENT" not in ical
