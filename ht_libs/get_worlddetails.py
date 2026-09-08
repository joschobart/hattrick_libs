"""Function to get data from worlddetails.xml."""

from bs4 import BeautifulSoup


def get_my_worlddetails(worlddetails_xml):
    """Get a complex dict object with important infos for a specific nation from worlddetails.xml"""

    world_dict = {}

    world_soup = BeautifulSoup(worlddetails_xml, "xml")

    LeagueID_tag = world_soup.find("LeagueID")
    LeagueName_tag = world_soup.find("LeagueName")
    LeagueSystemId_tag = world_soup.find("LeagueSystemId")  # 1 = male, 2 = female
    NumberOfLevels_tag = world_soup.find("NumberOfLevels")
    MatchRound_tag = world_soup.find("MatchRound")

    league_id, *_ = LeagueID_tag.contents
    league_name, *_ = LeagueName_tag.contents
    league_gender, *_ = LeagueSystemId_tag.contents  # 1 = male, 2 = female
    league_depth, *_ = NumberOfLevels_tag.contents
    season_round, *_ = MatchRound_tag.contents

    world_dict = {
        "league_id": league_id,
        "league_name": league_name,
        "league_gender": league_gender,
        "league_depth": league_depth,
        "season_round": season_round,
    }

    return world_dict
