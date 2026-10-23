"""Function to get data from worlddetails.xml."""

from bs4 import BeautifulSoup

from ._xml import optional_text


def get_my_worlddetails(worlddetails_xml):
    """Get a complex dict object with important infos for a specific nation from worlddetails.xml"""

    world_soup = BeautifulSoup(worlddetails_xml, "xml")

    league_id, *_ = world_soup.find("LeagueID").contents
    league_name, *_ = world_soup.find("LeagueName").contents
    league_depth, *_ = world_soup.find("NumberOfLevels").contents
    season_round, *_ = world_soup.find("MatchRound").contents

    # Only in some versions (2.0+: LeagueSystemID). 1 = male, 2 = female, "" if missing
    league_gender = optional_text(world_soup, "LeagueSystemID", "LeagueSystemId")

    return {
        "league_id": league_id,
        "league_name": league_name,
        "league_gender": league_gender,
        "league_depth": league_depth,
        "season_round": season_round,
    }


def get_country_flag_map(worlddetails_xml):
    """Map CHPP CountryID -> men's LeagueID (= flag id, as in <leagueid>.png).

    Women's teams all play in LeagueID 3000 and only carry their CountryID,
    so this map is how they find their flag.
    CountryID != LeagueID: CountryID 46 is Czechia, but LeagueID 46 is Switzerland!
    """
    soup = BeautifulSoup(worlddetails_xml, "xml")
    mapping = {}

    for league in soup.find_all("League"):
        if optional_text(league, "LeagueSystemID", "LeagueSystemId") == "2":
            continue  # the women's league itself has no flag of its own

        country_id = optional_text(league.find("Country"), "CountryID")
        league_id = optional_text(league, "LeagueID")
        if country_id and league_id:
            mapping[country_id] = league_id

    return mapping
