""" Function to get data from worlddetails.xml. """


from bs4 import BeautifulSoup


def get_my_worlddetails(worlddetails_xml):
    """Get a complex dict object with important infos for a specific nation from worlddetails.xml"""

    world_dict = {}

    world_soup = BeautifulSoup(worlddetails_xml, "xml")

    LeagueID_tag = world_soup.find("LeagueID")
    LeagueName_tag = world_soup.find("LeagueName")
    NumberOfLevels_tag = world_soup.find("NumberOfLevels")
    MatchRound_tag = world_soup.find("MatchRound")

    league_id, *_ = LeagueID_tag.contents
    league_name, *_ = LeagueName_tag.contents
    league_depth, *_ = NumberOfLevels_tag.contents
    season_round, *_ = MatchRound_tag.contents

    world_dict = {
        "league_id": league_id,
        "league_name": league_name,
        "league_depth": league_depth,
        "season_round": season_round,
    }

    return world_dict
