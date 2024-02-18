""" Functions to get data from matchdetails.xml. """


from bs4 import BeautifulSoup


def get_matchdetails(matchdetails_xml):
    """
    Get a complex dict object with important infos
    for a specific user from matchdetails.xml
    """

    match_dict = {}

    match_soup = BeautifulSoup(matchdetails_xml, "xml")

    Match_tag = match_soup.find("Match")
    HomeTeam_tag = match_soup.find("HomeTeam")
    AwayTeam_tag = match_soup.find("AwayTeam")
    Arena_tag = match_soup.find("Arena")

    match_id, *_ = Match_tag.MatchID.contents
    match_date, *_ = Match_tag.MatchDate.contents
    match_type, *_ = Match_tag.MatchType.contents

    home_team_id, *_ = HomeTeam_tag.HomeTeamID.contents
    home_team_name, *_ = HomeTeam_tag.HomeTeamName.contents
    try:
        home_team_goals, *_ = HomeTeam_tag.HomeGoals.contents
    except Exception:
        home_team_goals = ""

    away_team_id, *_ = AwayTeam_tag.AwayTeamID.contents
    away_team_name, *_ = AwayTeam_tag.AwayTeamName.contents
    try:
        away_team_goals, *_ = AwayTeam_tag.AwayGoals.contents
    except Exception:
        away_team_goals = ""

    arena_id, *_ = Arena_tag.ArenaID.contents
    arena_name, *_ = Arena_tag.ArenaName.contents

    match_dict = {
        "match_id": match_id,
        "match_date": match_date,
        "match_type": match_type,
        "home_team_id": home_team_id,
        "home_team_name": home_team_name,
        "home_team_goals": home_team_goals,
        "away_team_id": away_team_id,
        "away_team_name": away_team_name,
        "away_team_goals": away_team_goals,
        "arena_id": arena_id,
        "arena_name": arena_name,
    }

    return match_dict
