"""Tests for ht_libs.get_flags."""

from ht_libs import config, get_flags

TEAM_XML = """<HattrickData>
  <Teams>
    <Team>
      <TeamID>123</TeamID>
      <Flags>
        <HomeFlags>
          <Flag><LeagueId>46</LeagueId><CountryCode>CH</CountryCode></Flag>
          <Flag><LeagueId>99999</LeagueId><CountryCode>XX</CountryCode></Flag>
        </HomeFlags>
        <AwayFlags></AwayFlags>
      </Flags>
    </Team>
  </Teams>
</HattrickData>"""


def test_get_all_flags_matches_config():
    flags = get_flags.get_all_flags()
    assert len(flags) == len(config.ALL_FLAGS)
    assert all(isinstance(flag, tuple) for flag in flags)
    assert flags[0] == ("98", "Albania", "AL", "EU")


def test_all_flags_have_unique_league_ids():
    league_ids = [flag[0] for flag in config.ALL_FLAGS]
    assert len(league_ids) == len(set(league_ids))


def test_get_my_flags_known_and_unknown_league():
    teams = get_flags.get_my_flags(TEAM_XML)
    # LeagueId 99999 is not in ALL_FLAGS, so it must be ignored
    assert teams["123"]["flags_home"] == [("46", "Switzerland", "CH", "EU")]
    assert teams["123"]["flags_away"] == []


def test_get_missing_flags():
    missing = get_flags.get_missing_flags(TEAM_XML)["123"]
    assert len(missing["missing_home"]) == len(config.ALL_FLAGS) - 1
    assert ("46", "Switzerland", "CH", "EU") not in missing["missing_home"]
    assert len(missing["missing_away"]) == len(config.ALL_FLAGS)
