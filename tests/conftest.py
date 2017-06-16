# coding: utf-8
# data fixtures for functional tests

from datetime import date, time

import pytest

import marcottievents.models.common.enums as enums
import marcottievents.models.common.overview as mco
import marcottievents.models.common.personnel as mcp
import marcottievents.models.club as mc


@pytest.fixture
def comp_data():
    return {
        'domestic': {
            'name': "English Premier League",
            'level': 1,
            'country': mco.Countries(name="England", confederation=enums.ConfederationType.europe)
        },
        'international': {
            'name': "FIFA Club World Cup",
            'level': 1,
            'confederation': enums.ConfederationType.europe
        }
    }


@pytest.fixture
def season_data():
    return {
        'start_year': {
            'yr': 2012
        },
        'end_year': {
            'yr': 2013
        }
    }


@pytest.fixture
def venue_data():
    england = mco.Countries(name="England", confederation=enums.ConfederationType.europe)
    tz_london = mco.Timezones(name="Europe/London", offset=0.0, confederation=enums.ConfederationType.europe)
    return {
        "name": "Emirates Stadium",
        "city": "London",
        "country": england,
        "timezone": tz_london,
        "latitude": 51.555000,
        "longitude": -0.108611,
        "altitude": 41
    }


@pytest.fixture
def venue_config():
    return {
        "date": date(2006, 7, 22),
        "length": 105,
        "width": 68,
        "capacity": 60361,
        "seats": 60361,
        "surface": mco.Surfaces(description="Desso GrassMaster", type=enums.SurfaceType.hybrid)
    }


@pytest.fixture
def person_data():
    return {
        'generic': {
            'first_name': "John",
            'last_name': "Doe",
            'birth_date': date(1980, 1, 1),
            'country': mco.Countries(name="Portlandia", confederation=enums.ConfederationType.north_america)
        },
        'manager': [
            {
                'first_name': "Arsène",
                'last_name': "Wenger",
                'birth_date': date(1949, 10, 22),
                'country': mco.Countries(name="France", confederation=enums.ConfederationType.europe)
            },
            {
                'first_name': "Arthur",
                'middle_name': "Antunes",
                'last_name': "Coimbra",
                'nick_name': "Zico",
                'birth_date': date(1953, 3, 3),
                'country': mco.Countries(name="Brazil", confederation=enums.ConfederationType.south_america)
            }
        ],
        'player': [
            {
                'first_name': 'Miguel',
                'middle_name': 'Ángel',
                'last_name': 'Ponce',
                'second_last_name': 'Briseño',
                'birth_date': date(1989, 4, 12),
                'country': mco.Countries(name="Mexico", confederation=enums.ConfederationType.north_america),
                'order': enums.NameOrderType.middle
            },
            {
                'first_name': "Cristiano",
                'middle_name': "Ronaldo",
                'last_name': "Aveiro",
                'second_last_name': "dos Santos",
                'nick_name': "Cristiano Ronaldo",
                'birth_date': date(1985, 2, 5),
                'country': mco.Countries(name="Portugal", confederation=enums.ConfederationType.europe),
                'order': enums.NameOrderType.western
            },
            {
                'first_name': 'Heung-Min',
                'last_name': 'Son',
                'birth_date': date(1992, 7, 8),
                'country': mco.Countries(name="Korea Republic", confederation=enums.ConfederationType.asia),
                'order': enums.NameOrderType.eastern
            }
        ],
        'referee': [
            {
                'first_name': "Christopher",
                'middle_name': "J",
                'last_name': "Foy",
                'birth_date': date(1962, 11, 20),
                'country': mco.Countries(name="England", confederation=enums.ConfederationType.europe)
            },
            {
                'first_name': "Cüneyt",
                'last_name': "Çakır",
                'birth_date': date(1976, 11, 23),
                'country': mco.Countries(name="Turkey", confederation=enums.ConfederationType.europe)
            }
        ]
    }


@pytest.fixture
def position_data():
    return [
        mcp.Positions(name="Left back", type=enums.PositionType.defender),
        mcp.Positions(name="Forward", type=enums.PositionType.forward),
        mcp.Positions(name="Second striker", type=enums.PositionType.forward)
    ]


@pytest.fixture
def player_history_data():
    return [
        {
            'date': date(1996, 1, 1),
            'height': 1.70,
            'weight': 70
        },
        {
            'date': date(1998, 7, 15),
            'height': 1.74,
            'weight': 76
        },
        {
            'date': date(2001, 3, 11),
            'height': 1.76,
            'weight': 80
        }
    ]


@pytest.fixture
def match_condition_data():
    return {
        'kickoff_time': time(19, 30),
        'kickoff_temp': 15.0,
        'kickoff_humidity': 68.0,
        'kickoff_weather': enums.WeatherConditionType.partly_cloudy,
        'halftime_weather': enums.WeatherConditionType.clear,
        'fulltime_weather': enums.WeatherConditionType.windy_clear
    }


@pytest.fixture
def match_data(comp_data, season_data, venue_data, person_data):
    return {
        "date": date(2012, 12, 12),
        "competition": mco.DomesticCompetitions(**comp_data['domestic']),
        "season": mco.Seasons(**{k: mco.Years(**v) for k, v in list(season_data.items())}),
        "venue": mco.Venues(**venue_data),
        "home_manager": mcp.Managers(**person_data['manager'][0]),
        "away_manager": mcp.Managers(**person_data['manager'][1]),
        "referee": mcp.Referees(**person_data['referee'][0])
    }


@pytest.fixture
def club_data():
    england = mco.Countries(name="England", confederation=enums.ConfederationType.europe)
    france = mco.Countries(name="France", confederation=enums.ConfederationType.europe)
    tz_london = mco.Timezones(name="Europe/London", offset=0.0, confederation=enums.ConfederationType.europe)
    return {
        'date': date(2015, 1, 1),
        'competition': mco.DomesticCompetitions(name='Test Competition', level=1, country=england),
        'season': mco.Seasons(start_year=mco.Years(yr=2014), end_year=mco.Years(yr=2015)),
        'venue': mco.Venues(name="Emirates Stadium", city="London", country=england, timezone=tz_london),
        'home_team': mc.Clubs(name="Arsenal FC", country=england),
        'away_team': mc.Clubs(name="Lincoln City FC", country=england),
        'home_manager': mcp.Managers(first_name="Arsène", last_name="Wenger",
                                     birth_date=date(1949, 10, 22), country=france),
        'away_manager': mcp.Managers(first_name="Gary", last_name="Simpson",
                                     birth_date=date(1961, 4, 11), country=england),
        'referee': mcp.Referees(first_name="Mark", last_name="Clattenburg",
                                birth_date=date(1975, 3, 13), country=england)
    }


@pytest.fixture
def national_data():
    mexico = mco.Countries(name="Mexico", confederation=enums.ConfederationType.north_america)
    england = mco.Countries(name="England", confederation=enums.ConfederationType.europe)
    france = mco.Countries(name="France", confederation=enums.ConfederationType.europe)
    italy = mco.Countries(name="Italy", confederation=enums.ConfederationType.europe)
    tz_london = mco.Timezones(name="Europe/London", offset=0.0, confederation=enums.ConfederationType.europe)
    return {
        'date': date(1997, 11, 12),
        'competition': mco.InternationalCompetitions(name="International Cup", level=1,
                                                     confederation=enums.ConfederationType.fifa),
        'season': mco.Seasons(start_year=mco.Years(yr=1997), end_year=mco.Years(yr=1998)),
        'venue': mco.Venues(name="Emirates Stadium", city="London", country=england, timezone=tz_london),
        'home_team': france,
        'away_team': mexico,
        'home_manager': mcp.Managers(first_name="Arsène", last_name="Wenger",
                                     birth_date=date(1949, 10, 22), country=france),
        'away_manager': mcp.Managers(first_name="Gary", last_name="Simpson",
                                     birth_date=date(1961, 4, 11), country=england),
        'referee': mcp.Referees(first_name="Pierluigi", last_name="Collina",
                                birth_date=date(1960, 2, 13), country=italy)
    }


@pytest.fixture
def modifiers():
    return [
        {
            'modifier': "Left foot",
            'category': "Body Part"
        },
        {
            'modifier': "Right foot",
            'category': "Body Part"
        },
        {
            'modifier': "Foot",
            'category': "Body Part"
        },
        {
            'modifier': "Head",
            'category': "Body Part"
        },
        {
            'modifier': "Center Flank",
            'category': "Field Sector"
        },
        {
            'modifier': "Central Goal Area",
            'category': "Field Sector"
        },
        {
            'modifier': "Central Penalty Area",
            'category': "Field Sector"
        },
        {
            'modifier': "Volley",
            'category': "Shot Type"
        },
        {
            'modifier': "Saved",
            'category': "Shot Outcome"
        },
        {
            'modifier': "Lower Right",
            'category': "Goal Region"
        },
        {
            'modifier': "Wide of right post",
            'category': "Shot Direction"
        }
    ]
