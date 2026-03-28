"""Unit tests for the moon module."""

from unittest.mock import patch

from skyfield.api import load

from biodynamics.moon import Constellation, moon_constellation

ts = load.timescale()


def test_moon_constellation_returns_constellation():
    """Moon constellation returns a valid Constellation member."""
    t = ts.utc(2026, 3, 28, 12)
    result = moon_constellation(t)
    assert isinstance(result, Constellation)


def test_moon_constellation_varies_over_month():
    """Moon visits multiple constellations over a month."""
    constellations = set()
    for day in range(1, 29):
        t = ts.utc(2026, 3, day, 12)
        constellations.add(moon_constellation(t))
    assert len(constellations) >= 4


def test_moon_constellation_known_date():
    """Verify a known Moon position for a specific date."""
    t = ts.utc(2024, 1, 1, 12)
    result = moon_constellation(t)
    assert result == Constellation.LEO


@patch("biodynamics.moon._lahiri_ayanamsa", return_value=0.0)
def test_moon_constellation_zero_ayanamsa(mock_ayanamsa):
    """With zero ayanamsa, sidereal equals tropical."""
    t = ts.utc(2026, 3, 28, 12)
    result = moon_constellation(t)
    assert isinstance(result, Constellation)
    mock_ayanamsa.assert_called_once_with(t)
