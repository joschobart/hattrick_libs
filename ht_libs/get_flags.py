"""
Functions and helper-functions to get flags of a team.

Hattrick visualizes flags in two matrices on its website. One for home- and 
one for away-flags. Further it distinguishes between flags that were already 
captured and flags still to capture. This module fetches all relevant data 
from the hattrick data-model to reproduce the same information for a given team.
"""


from bs4 import BeautifulSoup

from . import config


def compile_flags_list(flags_xml):
    """
    Helper-Function to create a list of tuples (Flags)
    """

    flags_list = []
    flags_tuples = get_all_flags()

    for flag in flags_xml:
        league_id, *_ = flag.LeagueId.contents
        country_code, *_ = flag.CountryCode.contents

        for flag_tuple in flags_tuples:
            if league_id == flag_tuple[0]:
                league_name = flag_tuple[1]
                continent = flag_tuple[3]

                li = (league_id, league_name, country_code, continent)
                flags_list.append(li)

    return flags_list


def get_all_flags():
    """
    Get a list with all available flags from config.py
    """
    all_flags = config.ALL_FLAGS
    flags_tuples = []

    for flag in all_flags:
        flag = tuple(flag)
        flags_tuples.append(flag)

    return flags_tuples


def get_my_flags(teamdetails_xml):
    """
    Get a complex dict object with all specific flags (home/away)
    for a specific user
    """

    teams_dict = {}

    team_soup = BeautifulSoup(teamdetails_xml, "xml")

    # Finding all instances of tag
    # `Team`
    Team_tags = team_soup.find_all("Team")

    for Team_tag in Team_tags:
        team_id, *_ = Team_tag.TeamID.contents

        def get_place(place):
            if place == "home":
                flags = Team_tag.Flags.HomeFlags.find_all("Flag")
            else:
                flags = Team_tag.Flags.AwayFlags.find_all("Flag")

            all_flags = compile_flags_list(flags)

            return all_flags

        for x in ["home", "away"]:
            if x == "home":
                list_flags_home = get_place(x)
            else:
                list_flags_away = get_place(x)

        teams_dict[team_id] = {
            "flags_home": list_flags_home,
            "flags_away": list_flags_away,
        }

    return teams_dict


def get_missing_flags(teamdetails_xml):
    """
    Get a complex dict object with all specific flags (home/away)
    that are missing for a specific user
    """
    missing_flags_dict = {}

    all_flags = get_all_flags()
    all_my_flags = get_my_flags(teamdetails_xml)

    teams = get_my_flags(teamdetails_xml).keys()

    for team in teams:
        missing_home = list(set(all_flags) - set(all_my_flags[team]["flags_home"]))
        missing_away = list(set(all_flags) - set(all_my_flags[team]["flags_away"]))

        missing_flags_dict[team] = {
            "missing_home": missing_home,
            "missing_away": missing_away,
        }

    return missing_flags_dict
