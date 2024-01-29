"""
Functions and helper-functions to manage challenges for friendlies.

So far it is possible to get a list of challenged teams, to challenge one 
or multiple opponent teams as well as get information about fixures already
arranged.
"""


from bs4 import BeautifulSoup

from . import config


def is_challengeable(challengeable_xml):
    """
    Get a list object with challengeable teams
    from challengeable.xml
    """
    challengeable_teams = []

    challengeable_soup = BeautifulSoup(challengeable_xml, "xml")

    Opponent_tags = challengeable_soup.find_all("Opponent")

    for Opponent_tag in Opponent_tags:
        try:
            team_id, *_ = Opponent_tag.TeamId.contents
        except Exception as e:
            print(e)
            team_id = None

        try:
            _is_challengeable, *_ = Opponent_tag.IsChallengeable.contents
        except Exception as e:
            print(e)
            _is_challengeable = "False"

        if _is_challengeable == "True":
            challengeable_teams.append(team_id)

    return challengeable_teams


def do_challenge(
    my_teamid, session, challengeable_teams, match_type="1", match_place="1", is_weekend_friendly="0"
):
    """
    Takes a list of teams to challenge
    Returns status of challenges as dict
    """
    challenges = []

    for team_id in challengeable_teams:
        challenge = session.get(
            config.BASE_URL,
            params={
                "file": "challenges",
                "version": "1.6",
                "actionType": "challenge",
                "teamId": my_teamid,
                "opponentTeamId": team_id,
                "matchType": match_type,  # 0 is normal, 1 is cup rules
                "matchPlace": match_place,  # 0 is home, 1 is away, 2 is neutral
                "isWeekendFriendly": is_weekend_friendly,  # 0 is false, 1 is true
                "neutralArenaId": "",  # ArenaId for friendly on neutral ground
            },
        )

        challenge_soup = BeautifulSoup(challenge.text, "xml")

        Error_tag = challenge_soup.find_all("Error")

        if Error_tag is None:
            Opponent_tag = challenge_soup.find("Opponent")
            ArenaName_tag = challenge_soup.find("ArenaName")

            opponent_team_name, *_ = Opponent_tag.TeamName.contents
            arena_name, *_ = ArenaName_tag.contents

            challenges.append(
                {
                    "team_id": team_id,
                    "opponent_team_name": opponent_team_name,
                    "arena_name": arena_name,
                }
            )

    return challenges


def get_challenges(challenges_xml):
    """
    Get a dict object with challenged teams
    from challenges.xml
    """
    challenges = []

    challenged_teams_soup = BeautifulSoup(challenges_xml, "xml")

    Team_tag = challenged_teams_soup.find("Team")

    team_id, *_ = Team_tag.TeamID.contents
    team_name, *_ = Team_tag.TeamName.contents

    challenges = {"team_id": team_id, "team_name": team_name, "challenges": []}

    try:
        Challenge_tags = challenged_teams_soup.find_all("Challenge")

    except Exception as e:
        print(e)
        challenges = None

    else:
        for Challenge_tag in Challenge_tags:
            training_match_id, *_ = Challenge_tag.TrainingMatchID.contents

            try:
                match_id, *_ = Challenge_tag.MatchID.contents
            except Exception as e:
                print(e)
                match_id = ""

            match_time, *_ = Challenge_tag.MatchTime.contents
            friendly_type, *_ = Challenge_tag.FriendlyType.contents
            opponent_team_id, *_ = Challenge_tag.Opponent.TeamID.contents
            opponent_team_name, *_ = Challenge_tag.Opponent.TeamName.contents

            try:
                opponent_team_logo, *_ = Challenge_tag.Opponent.LogoURL.contents
            except Exception as e:
                print(e)
                opponent_team_logo = ""

            arena_id, *_ = Challenge_tag.Arena.ArenaID.contents
            arena_name, *_ = Challenge_tag.Arena.ArenaName.contents
            country_id, *_ = Challenge_tag.Country.CountryID.contents
            country_name, *_ = Challenge_tag.Country.CountryName.contents

            try:
                is_agreed, *_ = Challenge_tag.IsAgreed.contents
            except Exception as e:
                print(e)
                is_agreed = "False"

            challenges["challenges"].append(
                {
                    "training_match_id": training_match_id,
                    "match_id": match_id,
                    "match_time": match_time,
                    "friendly_type": friendly_type,
                    "opponent_team_id": opponent_team_id,
                    "opponent_team_name": opponent_team_name,
                    "opponent_team_logo": opponent_team_logo,
                    "arena_id": arena_id,
                    "arena_name": arena_name,
                    "country_id": country_id,
                    "country_name": country_name,
                    "is_agreed": is_agreed,
                }
            )

    return challenges
