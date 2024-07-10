""" Functions to get data from teamdetails.xml. """


from bs4 import BeautifulSoup


def get_teamdetails(teamdetails_xml):
    """
    Get a complex dict object with important infos
    for a specific user from teamdetails.xml
    """

    team_dict = {}

    team_soup = BeautifulSoup(teamdetails_xml, "xml")

    User_tag = team_soup.find("User")
    Team_tags = team_soup.find_all("Team")

    user_id, *_ = User_tag.UserID.contents

    try:
        login_name, *_ = User_tag.Loginname.contents
    except ValueError:
        login_name = "bot"

    supporter_tier, *_ = User_tag.SupporterTier.contents
    signup_date, *_ = User_tag.SignupDate.contents
    last_login_date, *_ = User_tag.LastLoginDate.contents

    team_dict["user"] = {
        "user_id": user_id,
        "login_name": login_name,
        "supporter_tier": supporter_tier,
        "signup_date": signup_date,
        "last_login_date": last_login_date,
    }

    for Team_tag in Team_tags:
        team_id, *_ = Team_tag.TeamID.contents
        team_name, *_ = Team_tag.TeamName.contents
        team_short, *_ = Team_tag.ShortTeamName.contents
        team_primary, *_ = Team_tag.IsPrimaryClub.contents
        team_country_id, *_ = Team_tag.League.LeagueID.contents

        try:
            (
                team_league_level_unit_id,
                *_,
            ) = Team_tag.LeagueLevelUnit.LeagueLevelUnitID.contents
        except AttributeError:
            team_league_level_unit_id = ""
            team_league_level_unit_name = ""
            team_league_level_unit_level = ""
        else:
            (
                team_league_level_unit_name,
                *_,
            ) = Team_tag.LeagueLevelUnit.LeagueLevelUnitName.contents
            (
                team_league_level_unit_level,
                *_,
            ) = Team_tag.LeagueLevelUnit.LeagueLevel.contents

        team_is_bot, *_ = Team_tag.BotStatus.IsBot.contents

        try:
            team_in_cup, *_ = Team_tag.Cup.StillInCup.contents
        except AttributeError:
            team_in_cup = "True"

        team_dict[team_id] = {
            "team_name": team_name,
            "team_short": team_short,
            "team_primary": team_primary,
            "team_country_id": team_country_id,
            "team_league_level_unit_id": team_league_level_unit_id,
            "team_league_level_unit_name": team_league_level_unit_name,
            "team_league_level_unit_level": team_league_level_unit_level,
            "team_is_bot": team_is_bot,
            "team_in_cup": team_in_cup,
        }

    return team_dict
