"""Function to get data from worlddetails.xml."""

from bs4 import BeautifulSoup


def _optional_text(soup, *names, default=""):
    """First text content of the first tag found under any of `names`, else default."""
    for name in names:
        tag = soup.find(name)
        if tag is not None and tag.contents:
            return tag.contents[0]
    return default


def get_my_worlddetails(worlddetails_xml):
    """Get a complex dict object with important infos for a specific nation from worlddetails.xml"""

    world_soup = BeautifulSoup(worlddetails_xml, "xml")

    LeagueID_tag = world_soup.find("LeagueID")
    LeagueName_tag = world_soup.find("LeagueName")
    NumberOfLevels_tag = world_soup.find("NumberOfLevels")
    MatchRound_tag = world_soup.find("MatchRound")

    league_id, *_ = LeagueID_tag.contents
    league_name, *_ = LeagueName_tag.contents
    league_depth, *_ = NumberOfLevels_tag.contents
    season_round, *_ = MatchRound_tag.contents

    league_gender = _optional_text(
        world_soup, "LeagueSystemId", "LeagueSystemID"
    )  # 1 = male, 2 = female

    return {
        "league_id": league_id,
        "league_name": league_name,
        "league_gender": league_gender,
        "league_depth": league_depth,
        "season_round": season_round,
    }
