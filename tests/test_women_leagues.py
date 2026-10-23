"""Women's leagues, tested against hand-trimmed real CHPP structures (2026-10)."""

from pathlib import Path

from ht_libs import get_teamdetails, get_worlddetails

FIXTURES = Path(__file__).parent / "fixtures"
TEAMS = (FIXTURES / "teamdetails_v3.9_two_teams.xml").read_bytes()
WORLD = (FIXTURES / "worlddetails_v2.0_trimmed.xml").read_bytes()


def test_country_flag_map_avoids_the_czech_swiss_trap():
    m = get_worlddetails.get_country_flag_map(WORLD)
    assert m["40"] == "46"  # Switzerland
    assert m["46"] == "52"  # Czechia, NOT the Swiss flag 🇨🇿≠🇨🇭
    assert m["12"] == "14"  # Netherlands
    assert m["1"] == "1"  # Sweden
    assert "3000" not in m.values()  # the women's league is never a flag


def test_worlddetails_v20_reads_league_system_id():
    d = get_worlddetails.get_my_worlddetails(WORLD)
    assert (d["league_id"], d["league_gender"], d["season_round"]) == ("1", "1", "14")


def test_women_team_has_gender_and_real_country():
    team = get_teamdetails.get_teamdetails(TEAMS)["3242724"]
    assert team["team_gender_id"] == "2"
    assert team["team_real_country_id"] == "40"
    assert team["team_country_id"] == "3000"  # LeagueID, unchanged behaviour


def test_men_team_unchanged_plus_gender():
    team = get_teamdetails.get_teamdetails(TEAMS)["628463"]
    assert team["team_gender_id"] == "1"
    assert team["team_country_id"] == "46"
    assert team["team_league_level_unit_id"] == "20934"


def test_both_teams_stay_separate():
    teams = get_teamdetails.get_teamdetails(TEAMS)
    assert {k for k in teams if k != "user"} == {"628463", "3242724"}
