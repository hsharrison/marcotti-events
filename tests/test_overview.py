# coding=utf-8
from datetime import date

import pytest
from sqlalchemy.sql import func
from sqlalchemy.exc import DataError, IntegrityError

import marcottievents.models.common.enums as enums
import marcottievents.models.common.overview as mco


def test_country_insert(session):
        """Country 001: Insert a single record into Countries table and verify data."""
        england = mco.Countries(name='England', confederation=enums.ConfederationType.europe)
        session.add(england)
        session.commit()

        country = session.query(mco.Countries).all()

        assert country[0].name == 'England'
        assert country[0].confederation.value == 'UEFA'
        assert repr(country[0]) == "<Country(id={0}, name=England, confed=UEFA)>".format(country[0].id)


def test_country_unicode_insert(session):
    """Country 002: Insert a single record with Unicode characters into Countries table and verify data."""
    ivory_coast = mco.Countries(name="Côte d'Ivoire", confederation=enums.ConfederationType.africa)
    session.add(ivory_coast)

    country = session.query(mco.Countries).filter_by(confederation=enums.ConfederationType.africa).one()

    assert country.name == "Côte d'Ivoire"
    assert country.confederation.value == 'CAF'


def test_country_name_overflow_error(session):
    """Country 003: Verify error if country name exceeds field length."""
    too_long_name = "blahblah" * 8
    too_long_country = mco.Countries(name=str(too_long_name), confederation=enums.ConfederationType.north_america)
    with pytest.raises(DataError):
        session.add(too_long_country)
        session.commit()


def test_competition_insert(session):
    """Competition 001: Insert a single record into Competitions table and verify data."""
    record = mco.Competitions(name="English Premier League", level=1)
    session.add(record)

    competition = session.query(mco.Competitions).filter_by(level=1).one()

    assert competition.name == "English Premier League"
    assert competition.level == 1


def test_competition_unicode_insert(session):
    """Competition 002: Insert a single record with Unicode characters into Competitions table and verify data."""
    record = mco.Competitions(name="Süper Lig", level=1)
    session.add(record)

    competition = session.query(mco.Competitions).one()

    assert competition.name == "Süper Lig"


def test_competition_name_overflow_error(session):
    """Competition 003: Verify error if competition name exceeds field length."""
    too_long_name = "leaguename" * 9
    record = mco.Competitions(name=str(too_long_name), level=2)
    with pytest.raises(DataError):
        session.add(record)
        session.commit()


def test_domestic_competition_insert(session):
    """Domestic Competition 001: Insert domestic competition record and verify data."""
    comp_name = "English Premier League"
    comp_country = "England"
    comp_level = 1
    record = mco.DomesticCompetitions(name=comp_name, level=comp_level, country=mco.Countries(
        name=comp_country, confederation=enums.ConfederationType.europe))
    session.add(record)

    competition = session.query(mco.DomesticCompetitions).one()

    assert repr(competition) == "<DomesticCompetition(name={0}, country={1}, level={2})>".format(
        comp_name, comp_country, comp_level)
    assert competition.name == comp_name
    assert competition.level == comp_level
    assert competition.country.name == comp_country


def test_international_competition_insert(session):
    """International Competition 001: Insert international competition record and verify data."""
    comp_name = "UEFA Champions League"
    comp_confed = enums.ConfederationType.europe
    record = mco.InternationalCompetitions(name=comp_name, level=1, confederation=comp_confed)
    session.add(record)

    competition = session.query(mco.InternationalCompetitions).one()

    assert repr(competition) == "<InternationalCompetition(name={0}, confederation={1})>".format(
        comp_name, comp_confed.value
    )
    assert competition.level == 1


def test_year_insert(session):
    """Year 001: Insert multiple years into Years table and verify data."""
    years_list = list(range(1990, 1994))
    for yr in years_list:
        record = mco.Years(yr=yr)
        session.add(record)

    years = session.query(mco.Years.yr).all()
    years_from_db = [x[0] for x in years]

    assert set(years_from_db) & set(years_list) == set(years_list)


def test_year_duplicate_error(session):
    """Year 002: Verify error if year is inserted twice in Years table."""
    for yr in range(1992, 1995):
        record = mco.Years(yr=yr)
        session.add(record)

    duplicate = mco.Years(yr=1994)
    with pytest.raises(IntegrityError):
        session.add(duplicate)
        session.commit()


def test_season_insert(session):
    """Season 001: Insert records into Seasons table and verify data."""
    yr_1994 = mco.Years(yr=1994)
    yr_1995 = mco.Years(yr=1995)

    season_94 = mco.Seasons(start_year=yr_1994, end_year=yr_1994)
    season_9495 = mco.Seasons(start_year=yr_1994, end_year=yr_1995)
    session.add(season_94)
    session.add(season_9495)

    seasons_from_db = [repr(obj) for obj in session.query(mco.Seasons).all()]
    seasons_test = ["<Season(1994)>", "<Season(1994-1995)>"]

    assert set(seasons_from_db) & set(seasons_test) == set(seasons_test)


def test_season_multiyr_search(session):
    """Season 002: Retrieve Season record using multi-year season name."""
    yr_1994 = mco.Years(yr=1994)
    yr_1995 = mco.Years(yr=1995)
    season_9495 = mco.Seasons(start_year=yr_1994, end_year=yr_1995)
    session.add(season_9495)

    record = session.query(mco.Seasons).filter(mco.Seasons.name == '1994-1995').one()
    assert repr(season_9495) == repr(record)


def test_season_multiyr_reference_date(session):
    """Season 003: Verify that reference date for season across two years is June 30."""
    yr_1994 = mco.Years(yr=1994)
    yr_1995 = mco.Years(yr=1995)
    season_9495 = mco.Seasons(start_year=yr_1994, end_year=yr_1995)
    session.add(season_9495)

    record = session.query(mco.Seasons).filter(mco.Seasons.start_year == yr_1994).one()
    assert record.reference_date == date(1995, 6, 30)


def test_season_singleyr_search(session):
    """Season 002: Retrieve Season record using multi-year season name."""
    yr_1994 = mco.Years(yr=1994)
    season_94 = mco.Seasons(start_year=yr_1994, end_year=yr_1994)
    session.add(season_94)

    record = session.query(mco.Seasons).filter(mco.Seasons.name == '1994').one()
    assert repr(season_94) == repr(record)


def test_season_singleyr_reference_date(session):
    """Season 005: Verify that reference date for season over one year is December 31."""
    yr_1994 = mco.Years(yr=1994)
    season_94 = mco.Seasons(start_year=yr_1994, end_year=yr_1994)
    session.add(season_94)

    record = session.query(mco.Seasons).filter(mco.Seasons.start_year == yr_1994).one()
    assert record.reference_date == date(1994, 12, 31)


def test_timezone_insert(session):
    """Timezone 001: Insert timezone records into Timezones table and verify data."""
    timezones = [
        mco.Timezones(name="Europe/Paris", offset=1, confederation=enums.ConfederationType.europe),
        mco.Timezones(name="America/New_York", offset=-5.0, confederation=enums.ConfederationType.north_america),
        mco.Timezones(name="Asia/Kathmandu", offset=+5.75, confederation=enums.ConfederationType.asia)
    ]
    session.add_all(timezones)

    tz_uefa = session.query(mco.Timezones).filter_by(confederation=enums.ConfederationType.europe).one()
    assert repr(tz_uefa) == "<Timezone(name=Europe/Paris, offset=+1.00, confederation=UEFA)>"

    stmt = session.query(func.min(mco.Timezones.offset).label('far_west')).subquery()
    tz_farwest = session.query(mco.Timezones).filter(mco.Timezones.offset == stmt.c.far_west).one()
    assert repr(tz_farwest) == "<Timezone(name=America/New_York, offset=-5.00, confederation=CONCACAF)>"

    stmt = session.query(func.max(mco.Timezones.offset).label('far_east')).subquery()
    tz_fareast = session.query(mco.Timezones).filter(mco.Timezones.offset == stmt.c.far_east).one()
    assert repr(tz_fareast) == "<Timezone(name=Asia/Kathmandu, offset=+5.75, confederation=AFC)>"


def test_venue_generic_insert(session, venue_data):
    """Venue 001: Insert generic venue records into Venues table and verify data."""
    session.add(mco.Venues(**venue_data))

    emirates = session.query(mco.Venues).one()

    assert repr(emirates) == "<Venue(name=Emirates Stadium, city=London, country=England)>"
    assert emirates.region is None
    assert emirates.latitude == 51.555000
    assert emirates.longitude == -0.108611
    assert emirates.altitude == 41
    assert repr(emirates.timezone) == "<Timezone(name=Europe/London, offset=+0.00, confederation=UEFA)>"


def test_venue_empty_coordinates(session, venue_data):
    """Venue 002: Verify that lat/long/alt coordinates are zeroed if not present in Venues object definition."""
    revised_venue_data = {key: value for key, value in list(venue_data.items())
                          if key not in ['latitude', 'longitude', 'altitude']}
    session.add(mco.Venues(**revised_venue_data))

    emirates = session.query(mco.Venues).one()

    assert emirates.latitude == 0.000000
    assert emirates.longitude == 0.000000
    assert emirates.altitude == 0


def test_venue_latitude_error(session, venue_data):
    """Venue 003: Verify error if latitude of match venue exceeds range."""
    for direction in [-1, 1]:
        venue_data['latitude'] = 92.123456 * direction
        venue = mco.Venues(**venue_data)
        with pytest.raises(IntegrityError):
            session.add(venue)
            session.commit()
        session.rollback()


def test_venue_longitude_error(session, venue_data):
    """Venue 004: Verify error if longitude of match venue exceeds range."""
    for direction in [-1, 1]:
        venue_data['longitude'] = 200.000000 * direction
        venue = mco.Venues(**venue_data)
        with pytest.raises(IntegrityError):
            session.add(venue)
            session.commit()
        session.rollback()


def test_venue_altitude_error(session, venue_data):
    """Venue 005: Verify error if altitude of match venue is out of range."""
    for out_of_range in [-205, 4600]:
        venue_data['altitude'] = out_of_range
        venue = mco.Venues(**venue_data)
        with pytest.raises(IntegrityError):
            session.add(venue)
            session.commit()
        session.rollback()


def test_venue_history_insert(session, venue_data, venue_config):
    """Venue 006: Insert venue history data into VenueHistory model and verify data."""
    emirates = mco.Venues(**venue_data)
    venue_config['venue'] = emirates
    emirates_config = mco.VenueHistory(**venue_config)
    session.add(emirates_config)

    record = session.query(mco.VenueHistory).one()

    assert repr(record) == "<VenueHistory(name=Emirates Stadium, date=2006-07-22, " \
                           "length=105, width=68, capacity=60361)>"
    assert record.seats == 60361
    assert record.surface.description == "Desso GrassMaster"
    assert record.surface.type == enums.SurfaceType.hybrid


def test_venue_history_empty_numbers(session, venue_data, venue_config):
    """Venue 007: Verify that length/width/capacity/seats fields are set to default if missing in VenueHistory data."""
    emirates = mco.Venues(**venue_data)
    venue_config['venue'] = emirates
    revised_venue_config = {key: value for key, value in list(venue_config.items())
                            if key not in ['length', 'width', 'capacity', 'seats']}
    emirates_config = mco.VenueHistory(**revised_venue_config)
    session.add(emirates_config)

    record = session.query(mco.VenueHistory).one()

    assert record.length == 105
    assert record.width == 68
    assert record.capacity == 0
    assert record.seats == 0


def test_venue_history_field_dimension_error(session, venue_data, venue_config):
    """Venue 007: Verify error if length/width fields in VenueHistory data are out of range."""
    emirates = mco.Venues(**venue_data)
    venue_config['venue'] = emirates
    for field, values in zip(['length', 'width'], [(85, 125), (40, 95)]):
        for out_of_range in values:
            venue_config[field] = out_of_range
            emirates_config = mco.VenueHistory(**venue_config)
            with pytest.raises(IntegrityError):
                session.add(emirates_config)
                session.commit()
            session.rollback()


def test_venue_history_capacity_error(session, venue_data, venue_config):
    """Venue 007: Verify error if length/width fields in VenueHistory data are out of range."""
    emirates = mco.Venues(**venue_data)
    venue_config['venue'] = emirates
    for field in ['capacity', 'seats']:
        new_venue_config = dict(venue_config, **{field: -1})
        emirates_config = mco.VenueHistory(**new_venue_config)
        with pytest.raises(IntegrityError):
            session.add(emirates_config)
            session.commit()
        session.rollback()


def test_surface_generic_insert(session):
    """Playing Surface 001: Insert playing surface data into Surfaces model and verify data."""
    surfaces = [
        mco.Surfaces(description="Perennial ryegrass", type=enums.SurfaceType.natural),
        mco.Surfaces(description="Desso GrassMaster", type=enums.SurfaceType.hybrid),
        mco.Surfaces(description="FieldTurf", type=enums.SurfaceType.artificial)
    ]
    session.add_all(surfaces)

    natural = session.query(mco.Surfaces).filter_by(type=enums.SurfaceType.natural).one()

    assert repr(natural) == "<Surface(description=Perennial ryegrass, type=Natural)>"


def test_surface_empty_description_error(session):
    """Playing Surface 002: Verify error if description field for Surfaces model is empty."""
    surface = mco.Surfaces(type=enums.SurfaceType.natural)
    with pytest.raises(IntegrityError):
        session.add(surface)
        session.commit()
