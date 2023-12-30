""" Functions and to get data about the series/ league of a team. """


from bs4 import BeautifulSoup


def get_my_series(search_series_xml):
    """
    Get a dict object with important infos
    for a specific series from search.xml
    """
    series_soup = BeautifulSoup(search_series_xml, "xml")

    SearchLeagueID_tag = series_soup.find("SearchLeagueID")
    ResultName_tag = series_soup.find("ResultName")
    ResultID_tag = series_soup.find("ResultID")

    nation_id, *_ = SearchLeagueID_tag.contents
    series_name, *_ = ResultName_tag.contents
    series_id, *_ = ResultID_tag.contents

    series_dict = {
        "nation_id": nation_id,
        "series_name": series_name,
        "series_id": series_id,
    }

    return series_dict


def get_teams_in_series(teams_in_series_xml):
    """
    Get a complex dict object with all important infos
    for a specific series aggregated from search.xml and
    leaguedetails.xml
    """
    tis_soup = BeautifulSoup(teams_in_series_xml, "xml")

    LeagueID_tag = tis_soup.find("LeagueID")
    LeagueLevelUnitName_tag = tis_soup.find("LeagueLevelUnitName")
    LeagueLevelUnitID_tag = tis_soup.find("LeagueLevelUnitID")

    Team_tags = tis_soup.find_all("Team")

    nation_id, *_ = LeagueID_tag.contents
    series_name, *_ = LeagueLevelUnitName_tag.contents
    series_id, *_ = LeagueLevelUnitID_tag.contents

    series_dict = {
        "nation_id": nation_id,
        "series_name": series_name,
        "series_id": series_id,
        "series_teams": [],
    }

    for Team_tag in Team_tags:
        team_id, *_ = Team_tag.TeamID.contents

        series_dict["series_teams"].append(team_id)

    return series_dict
