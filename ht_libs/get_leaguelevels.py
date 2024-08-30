""" Function to get data from leaguelevels.xml. """


from bs4 import BeautifulSoup


def get_leaguelevels(leaguelevels_xml):
    """Get a complex dict object with important league level-infos for a specific country from leaguelevels.xml"""

    ll_dict = {}

    ll_soup = BeautifulSoup(leaguelevels_xml, "xml")

    LeagueID_tag = ll_soup.find("LeagueID")
    NrOfLeagueLevels_tag = ll_soup.find("NrOfLeagueLevels")
    Season_tag = ll_soup.find("Season")

    league_id, *_ = LeagueID_tag.contents
    league_depth, *_ = NrOfLeagueLevels_tag.contents
    season_round, *_ = Season_tag.contents

    ll_dict = {
        "league_id": league_id,
        "league_depth": league_depth,
        "season_round": season_round,
        "league_levels": [],
    }

    LeagueLevelItem_tags = ll_soup.find_all("LeagueLevelItem")

    for LeagueLevelItem_tag in LeagueLevelItem_tags:
        league_level, *_ = LeagueLevelItem_tag.LeagueLevel.contents
        nbr_llus, *_ = LeagueLevelItem_tag.NrOfLeagueLevelUnits.contents
        lluid_list, *_ = LeagueLevelItem_tag.LeagueLevelUnitIdList.contents
        nbr_teams, *_ = LeagueLevelItem_tag.NrOfTeams.contents
        nbr_spsps, *_ = LeagueLevelItem_tag.NrOfSharedPromotionSlotsPerSeries.contents
        nbr_dpsps, *_ = LeagueLevelItem_tag.NrOfDirectPromotionSlotsPerSeries.contents
        (
            nbr_qpsps,
            *_,
        ) = LeagueLevelItem_tag.NrOfQualificationPromotionSlotsPerSeries.contents
        nbr_ddsps, *_ = LeagueLevelItem_tag.NrOfDirectDemotionSlotsPerSeries.contents
        (
            nbr_qdsps,
            *_,
        ) = LeagueLevelItem_tag.NrOfQualificationDemotionSlotsPerSeries.contents

        ll_dict["league_levels"].append(
            {
                "league_level": league_level,
                "nbr_llus": nbr_llus,
                "lluid_list": [e.strip("\n") for e in list(lluid_list.split(","))],
                "nbr_teams": nbr_teams,
                "nbr_spsps": nbr_spsps,
                "nbr_dpsps": nbr_dpsps,
                "nbr_qpsps": nbr_qpsps,
                "nbr_ddsps": nbr_ddsps,
                "nbr_qdsps": nbr_qdsps,
            }
        )

    return ll_dict
