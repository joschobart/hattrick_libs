""" Functions to get data from matches. """


from bs4 import BeautifulSoup


def get_matches(matches_xml):
    """
    Get a complex dict object with future and past matches
    and corresponding details for a specific user from matches
    """

    match_dict = {}

    match_soup = BeautifulSoup(matches_xml, "xml")

    Team_tag = match_soup.find("TeamID")
    Match_tags = match_soup.find_all("Match")

    team_id, *_ = Team_tag.contents

    matches_dict = {
        "team_id": team_id,
        "matches": [],
    }

    for Match_tag in Match_tags:
        match_id, *_ = Match_tag.MatchID.contents
        home_team_id, *_ = Match_tag.HomeTeam.HomeTeamID.contents
        away_team_id, *_ = Match_tag.AwayTeam.AwayTeamID.contents
        match_date, *_ = Match_tag.MatchDate.contents
        source_system, *_ = Match_tag.SourceSystem.contents
        match_type, *_ = Match_tag.MatchType.contents
        match_status, *_ = Match_tag.Status.contents

        matches_dict["matches"].append({
            "match_id": match_id,
            "home_team_id": home_team_id,
            "away_team_id": away_team_id,
            "match_date": match_date,
            "source_system": source_system,
            "match_type": match_type,
            "match_status": match_status,
        })

    return matches_dict
