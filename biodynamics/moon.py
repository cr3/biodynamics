"""Moon sidereal zodiac calculations using Skyfield."""

from enum import Enum
from pathlib import Path

from skyfield.api import Loader
from skyfield.timelib import Time

LOAD = Loader(Path(__file__).parent / "data")

# Lahiri ayanamsa at J2000.0 epoch and its annual precession rate.
_LAHIRI_AYANAMSA_J2000 = 23.85
_PRECESSION_PER_YEAR = 50.29 / 3600  # arcseconds to degrees


class Constellation(Enum):
    """Zodiac constellations in ecliptic order."""

    ARIES = "Aries"
    TAURUS = "Taurus"
    GEMINI = "Gemini"
    CANCER = "Cancer"
    LEO = "Leo"
    VIRGO = "Virgo"
    LIBRA = "Libra"
    SCORPIO = "Scorpio"
    SAGITTARIUS = "Sagittarius"
    CAPRICORN = "Capricorn"
    AQUARIUS = "Aquarius"
    PISCES = "Pisces"


# Ordered list matching 0-11 index to 30° segments.
_CONSTELLATIONS = list(Constellation)


def _lahiri_ayanamsa(t: Time) -> float:
    """Return the Lahiri ayanamsa in degrees for a Skyfield Time."""
    years_since_j2000 = t.tdb - 2451545.0  # days
    years = years_since_j2000 / 365.25
    return _LAHIRI_AYANAMSA_J2000 + years * _PRECESSION_PER_YEAR


def moon_constellation(t: Time) -> Constellation:
    """Return the sidereal zodiac constellation of the Moon.

    Uses the Lahiri ayanamsa to convert the Moon's tropical ecliptic
    longitude to sidereal coordinates, then maps to one of twelve
    equal 30° zodiac segments.
    """
    eph = LOAD("de421.bsp")
    earth = eph["earth"]
    moon = eph["moon"]

    astrometric = earth.at(t).observe(moon)
    _, lon, _ = astrometric.apparent().ecliptic_latlon()

    tropical_lon = lon.degrees
    sidereal_lon = (tropical_lon - _lahiri_ayanamsa(t)) % 360

    index = int(sidereal_lon // 30)
    return _CONSTELLATIONS[index]
