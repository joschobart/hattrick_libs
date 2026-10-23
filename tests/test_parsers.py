"""Tests for the XML parser modules of ht_libs."""

from pathlib import Path

from ht_libs import (
    get_leaguelevels,
    get_matchdetails,
    get_matches,
    get_series,
    get_teamdetails,
    get_trainer_avatar,
    get_worlddetails,
    request_token_status,
)

FIXTURES = Path(__file__).parent / "fixtures"


# --- worlddetails -----------------------------------------------------------

WORLD_XML = """<HattrickData>
  <LeagueList>
    <League>
      <LeagueID>46</LeagueID>
      <LeagueName>Schweiz</LeagueName>
      <LeagueSystemId>1</LeagueSystemId>
      <NumberOfLevels>8</NumberOfLevels>
      <MatchRound>7</MatchRound>
    </League>
  </LeagueList>
</HattrickData>"""


def test_worlddetails():
    assert get_worlddetails.get_my_worlddetails(WORLD_XML) == {
        "league_id": "46",
        "league_name": "Schweiz",
        "league_gender": "1",
        "league_depth": "8",
        "season_round": "7",
    }


# --- leaguelevels -----------------------------------------------------------


def _level_item(level, units, unit_ids, teams):
    # distinct slot numbers (0-4) so a mixed-up mapping would be caught
    return f"""
    <LeagueLevelItem>
      <LeagueLevel>{level}</LeagueLevel>
      <NrOfLeagueLevelUnits>{units}</NrOfLeagueLevelUnits>
      <LeagueLevelUnitIdList>{unit_ids}</LeagueLevelUnitIdList>
      <NrOfTeams>{teams}</NrOfTeams>
      <NrOfSharedPromotionSlotsPerSeries>0</NrOfSharedPromotionSlotsPerSeries>
      <NrOfDirectPromotionSlotsPerSeries>1</NrOfDirectPromotionSlotsPerSeries>
      <NrOfQualificationPromotionSlotsPerSeries>2</NrOfQualificationPromotionSlotsPerSeries>
      <NrOfDirectDemotionSlotsPerSeries>3</NrOfDirectDemotionSlotsPerSeries>
      <NrOfQualificationDemotionSlotsPerSeries>4</NrOfQualificationDemotionSlotsPerSeries>
    </LeagueLevelItem>"""


LEAGUELEVELS_XML = f"""<HattrickData>
  <LeagueID>46</LeagueID>
  <Season>7</Season>
  <NrOfLeagueLevels>2</NrOfLeagueLevels>
  <LeagueLevelList>{_level_item(1, 1, "100", 8)}{_level_item(2, 3, "101,102,103", 8)}
  </LeagueLevelList>
</HattrickData>"""


def test_leaguelevels():
    result = get_leaguelevels.get_leaguelevels(LEAGUELEVELS_XML)
    assert result["league_id"] == "46"
    assert result["league_depth"] == "2"
    assert result["season_round"] == "7"
    assert len(result["league_levels"]) == 2
    assert result["league_levels"][1] == {
        "league_level": "2",
        "nbr_llus": "3",
        "lluid_list": ["101", "102", "103"],
        "nbr_teams": "8",
        "nbr_spsps": "0",
        "nbr_dpsps": "1",
        "nbr_qpsps": "2",
        "nbr_ddsps": "3",
        "nbr_qdsps": "4",
    }


# --- matches ----------------------------------------------------------------

MATCHES_XML = """<HattrickData>
  <Team>
    <TeamID>123</TeamID>
    <MatchList>
      <Match>
        <MatchID>1001</MatchID>
        <HomeTeam><HomeTeamID>123</HomeTeamID></HomeTeam>
        <AwayTeam><AwayTeamID>456</AwayTeamID></AwayTeam>
        <MatchDate>2026-10-24 15:00:00</MatchDate>
        <SourceSystem>Hattrick</SourceSystem>
        <MatchType>1</MatchType>
        <Status>UPCOMING</Status>
      </Match>
    </MatchList>
  </Team>
</HattrickData>"""


def test_matches():
    result = get_matches.get_matches(MATCHES_XML)
    assert result["team_id"] == "123"
    assert result["matches"] == [
        {
            "match_id": "1001",
            "home_team_id": "123",
            "away_team_id": "456",
            "match_date": "2026-10-24 15:00:00",
            "source_system": "Hattrick",
            "match_type": "1",
            "match_status": "UPCOMING",
        }
    ]


# --- matchdetails -----------------------------------------------------------

MATCHDETAILS_PLAYED_XML = """<HattrickData>
  <Match>
    <MatchID>1001</MatchID>
    <MatchType>1</MatchType>
    <MatchDate>2026-10-17 15:00:00</MatchDate>
    <HomeTeam><HomeTeamID>123</HomeTeamID><HomeTeamName>FC Home</HomeTeamName><HomeGoals>2</HomeGoals></HomeTeam>
    <AwayTeam><AwayTeamID>456</AwayTeamID><AwayTeamName>FC Away</AwayTeamName><AwayGoals>1</AwayGoals></AwayTeam>
    <Arena><ArenaID>789</ArenaID><ArenaName>Test Arena</ArenaName></Arena>
    <Scorers>
      <Goal Index="12">
        <ScorerPlayerID>5</ScorerPlayerID>
        <ScorerPlayerName>Test Player</ScorerPlayerName>
        <ScorerTeamID>123</ScorerTeamID>
        <ScorerMinute>42</ScorerMinute>
      </Goal>
    </Scorers>
  </Match>
</HattrickData>"""

MATCHDETAILS_UPCOMING_XML = """<HattrickData>
  <Match>
    <MatchID>1002</MatchID>
    <MatchType>1</MatchType>
    <MatchDate>2026-10-24 15:00:00</MatchDate>
    <HomeTeam><HomeTeamID>123</HomeTeamID><HomeTeamName>FC Home</HomeTeamName></HomeTeam>
    <AwayTeam><AwayTeamID>456</AwayTeamID><AwayTeamName>FC Away</AwayTeamName></AwayTeam>
    <Arena><ArenaID>789</ArenaID><ArenaName>Test Arena</ArenaName></Arena>
  </Match>
</HattrickData>"""


def test_matchdetails_played_match():
    result = get_matchdetails.get_matchdetails(MATCHDETAILS_PLAYED_XML)
    assert result["match_id"] == "1001"
    assert result["home_team_name"] == "FC Home"
    assert result["home_team_goals"] == "2"
    assert result["away_team_goals"] == "1"
    assert result["arena_name"] == "Test Arena"
    assert len(result["goals"]) == 1
    goal = result["goals"][0]
    assert goal["goal_scorer_name"] == "Test Player"
    assert goal["goal_scorer_teamid"] == "123"
    assert goal["goal_score_minute"] == "42"
    assert goal["goal_number"] == "12"


def test_matchdetails_upcoming_match_has_no_goals():
    result = get_matchdetails.get_matchdetails(MATCHDETAILS_UPCOMING_XML)
    assert result["home_team_goals"] == ""
    assert result["away_team_goals"] == ""
    assert result["goals"] == []


def test_matchdetails_accepts_utf8_bytes():
    xml = MATCHDETAILS_UPCOMING_XML.replace("FC Home", "FC Vorwärts")
    result = get_matchdetails.get_matchdetails(xml.encode("utf-8"))
    assert result["home_team_name"] == "FC Vorwärts"


# --- series -----------------------------------------------------------------

SEARCH_XML = """<HattrickData>
  <SearchParams>
    <SearchType>3</SearchType>
    <SearchString>II.1</SearchString>
    <SearchLeagueID>46</SearchLeagueID>
  </SearchParams>
  <SearchResults>
    <Result><ResultID>100</ResultID><ResultName>II.1</ResultName></Result>
  </SearchResults>
</HattrickData>"""

LEAGUEDETAILS_XML = """<HattrickData>
  <LeagueID>46</LeagueID>
  <LeagueLevelUnitID>100</LeagueLevelUnitID>
  <LeagueLevelUnitName>II.1</LeagueLevelUnitName>
  <Team><TeamID>123</TeamID></Team>
  <Team><TeamID>456</TeamID></Team>
</HattrickData>"""


def test_get_my_series():
    assert get_series.get_my_series(SEARCH_XML) == {
        "nation_id": "46",
        "series_name": "II.1",
        "series_id": "100",
    }


def test_get_teams_in_series():
    assert get_series.get_teams_in_series(LEAGUEDETAILS_XML) == {
        "nation_id": "46",
        "series_name": "II.1",
        "series_id": "100",
        "series_teams": ["123", "456"],
    }


# --- teamdetails ------------------------------------------------------------

TEAMDETAILS_XML = """<HattrickData>
  <User>
    <UserID>42</UserID>
    <Loginname>test_manager</Loginname>
    <SupporterTier>gold</SupporterTier>
    <SignupDate>2020-01-01 10:00:00</SignupDate>
    <LastLoginDate>2026-10-22 08:00:00</LastLoginDate>
  </User>
  <Teams>
    <Team>
      <TeamID>123</TeamID>
      <TeamName>FC Test</TeamName>
      <ShortTeamName>FCT</ShortTeamName>
      <IsPrimaryClub>True</IsPrimaryClub>
      <League><LeagueID>46</LeagueID></League>
      <LeagueSystemId>1</LeagueSystemId>
      <LeagueLevelUnit>
        <LeagueLevelUnitID>100</LeagueLevelUnitID>
        <LeagueLevelUnitName>II.1</LeagueLevelUnitName>
        <LeagueLevel>2</LeagueLevel>
      </LeagueLevelUnit>
      <BotStatus><IsBot>False</IsBot></BotStatus>
      <Cup><StillInCup>False</StillInCup></Cup>
    </Team>
    <Team>
      <TeamID>456</TeamID>
      <TeamName>FC Minimal</TeamName>
      <ShortTeamName>FCM</ShortTeamName>
      <IsPrimaryClub>False</IsPrimaryClub>
      <League><LeagueID>46</LeagueID></League>
      <BotStatus><IsBot>False</IsBot></BotStatus>
    </Team>
  </Teams>
</HattrickData>"""


def test_teamdetails_user_and_full_team():
    result = get_teamdetails.get_teamdetails(TEAMDETAILS_XML)
    assert result["user"] == {
        "user_id": "42",
        "login_name": "test_manager",
        "supporter_tier": "gold",
        "signup_date": "2020-01-01 10:00:00",
        "last_login_date": "2026-10-22 08:00:00",
    }
    assert result["123"] == {
        "team_name": "FC Test",
        "team_short": "FCT",
        "team_primary": "True",
        "team_country_id": "46",
        "league_gender": "1",
        "team_league_level_unit_id": "100",
        "team_league_level_unit_name": "II.1",
        "team_league_level_unit_level": "2",
        "team_in_cup": "False",
        "team_is_bot": "False",
        "team_gender_id": "",  # the hand-made XML has no GenderID
        "team_real_country_id": "",  # ...and no Country block
    }


def test_teamdetails_minimal_team_uses_defaults():
    team = get_teamdetails.get_teamdetails(TEAMDETAILS_XML)["456"]
    assert team["league_gender"] == ""
    assert team["team_league_level_unit_id"] == ""
    assert team["team_league_level_unit_name"] == ""
    assert team["team_league_level_unit_level"] == ""
    assert team["team_in_cup"] == "True"


def test_teamdetails_empty_loginname_becomes_bot():
    xml = TEAMDETAILS_XML.replace(
        "<Loginname>test_manager</Loginname>", "<Loginname></Loginname>"
    )
    assert get_teamdetails.get_teamdetails(xml)["user"]["login_name"] == "bot"


def test_worlddetails_real_chpp_v19_response_without_league_system():
    # recorded from CHPP 2026-10-22, trimmed to one league
    xml = (FIXTURES / "worlddetails_v1.9_one_league.xml").read_bytes()
    d = get_worlddetails.get_my_worlddetails(xml)
    assert d["league_id"] == "1"
    assert d["league_name"] == "Sweden"
    assert d["league_depth"] == "6"
    assert d["season_round"] == "14"
    assert d["league_gender"] == ""


# --- trainer avatar ---------------------------------------------------------

STAFFAVATARS_XML = """<HattrickData>
  <Trainer>
    <TrainerId>77</TrainerId>
    <Avatar>
      <Layer x="9" y="10"><Image>/Img/Avatar/backgrounds/bg_blue.png</Image></Layer>
      <Layer x="4" y="5"><Image>/Img/Avatar/faces/f1.png</Image></Layer>
    </Avatar>
  </Trainer>
</HattrickData>"""


def test_trainer_avatar_offsets_layers():
    result = get_trainer_avatar.get_trainer_avatar(STAFFAVATARS_XML)
    assert result["trainer_id"] == "77"
    # x - 4 and y - 5
    assert result["avatar_background"] == {
        "left": "5px",
        "top": "5px",
        "url": "/Img/Avatar/backgrounds/bg_blue.png",
    }
    assert result["avatar_face"] == {
        "left": "0px",
        "top": "0px",
        "url": "/Img/Avatar/faces/f1.png",
    }
    assert "avatar_hair" not in result


# --- token status -----------------------------------------------------------


def test_request_token_status_current_behaviour():
    result = request_token_status.request_token_status(
        "<HattrickData><UserID>42</UserID></HattrickData>"
    )
    assert result["user_id"] == ["42"]
