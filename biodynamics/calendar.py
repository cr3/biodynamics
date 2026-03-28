"""Biodynamic planting calendar generation."""

from datetime import date, timedelta

from icalendar import Calendar, Event
from skyfield.api import load

from biodynamics.moon import Constellation, moon_constellation


class PlantType:
    """Plant types associated with classical elements."""

    FRUIT = "🍎"
    ROOT = "🥕"
    FLOWER = "🌸"
    LEAF = "🌿"


# Mapping from constellation to plant type via classical elements.
CONSTELLATION_PLANT_TYPE = {
    # Fire -> Fruit
    Constellation.ARIES: PlantType.FRUIT,
    Constellation.LEO: PlantType.FRUIT,
    Constellation.SAGITTARIUS: PlantType.FRUIT,
    # Earth -> Root
    Constellation.TAURUS: PlantType.ROOT,
    Constellation.VIRGO: PlantType.ROOT,
    Constellation.CAPRICORN: PlantType.ROOT,
    # Air -> Flower
    Constellation.GEMINI: PlantType.FLOWER,
    Constellation.LIBRA: PlantType.FLOWER,
    Constellation.AQUARIUS: PlantType.FLOWER,
    # Water -> Leaf
    Constellation.CANCER: PlantType.LEAF,
    Constellation.SCORPIO: PlantType.LEAF,
    Constellation.PISCES: PlantType.LEAF,
}


def plant_type(d: date) -> str:
    """Return the biodynamic plant type for a given date.

    >>> from datetime import date
    >>> plant_type(date(2026, 3, 28)) in ('🍎', '🥕', '🌸', '🌿')
    True
    """
    ts = load.timescale()
    # Use noon UTC as the representative time for the day.
    t = ts.utc(d.year, d.month, d.day, 12)
    constellation = moon_constellation(t)
    return CONSTELLATION_PLANT_TYPE[constellation]


def generate_calendar(start: date, end: date) -> Calendar:
    """Generate an iCalendar with biodynamic plant type events.

    Each day in the range [start, end) gets an all-day event whose
    summary is the plant type for that day.
    """
    cal = Calendar()
    cal.add("prodid", "-//biodynamics//EN")
    cal.add("version", "2.0")

    current = start
    while current < end:
        ptype = plant_type(current)

        event = Event()
        event.add("summary", ptype)
        event.add("dtstart", current)
        event.add("dtend", current + timedelta(days=1))
        cal.add_component(event)

        current += timedelta(days=1)

    return cal
