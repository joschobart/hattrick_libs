"""Tests for ht_libs.do_challenge."""

from types import SimpleNamespace

from ht_libs import config, do_challenge

CHALLENGEABLE_XML = """<HattrickData>
  <ChallengeableResult>
    <Opponent><TeamId>111</TeamId><IsChallengeable>True</IsChallengeable></Opponent>
    <Opponent><TeamId>222</TeamId><IsChallengeable>False</IsChallengeable></Opponent>
    <Opponent><TeamId>333</TeamId></Opponent>
  </ChallengeableResult>
</HattrickData>"""

CHALLENGE_OK_XML = """<HattrickData>
  <Opponent><TeamName>FC Opponent</TeamName></Opponent>
  <ArenaName>Opponent Arena</ArenaName>
</HattrickData>"""

CHALLENGE_ERROR_XML = """<HattrickData>
  <Error>Team is not challengeable</Error>
</HattrickData>"""

CHALLENGES_XML = """<HattrickData>
  <Team>
    <TeamID>123</TeamID>
    <TeamName>FC Test</TeamName>
    <ChallengesByMe>
      <Challenge>
        <TrainingMatchID>9001</TrainingMatchID>
        <MatchID>1001</MatchID>
        <MatchTime>2026-10-29 19:00:00</MatchTime>
        <FriendlyType>1</FriendlyType>
        <Opponent>
          <TeamID>456</TeamID>
          <TeamName>FC Opponent</TeamName>
          <LogoURL>//example.invalid/logo.png</LogoURL>
        </Opponent>
        <Arena><ArenaID>789</ArenaID><ArenaName>Opponent Arena</ArenaName></Arena>
        <Country><CountryID>46</CountryID><CountryName>Switzerland</CountryName></Country>
        <IsAgreed>True</IsAgreed>
      </Challenge>
      <Challenge>
        <TrainingMatchID>9002</TrainingMatchID>
        <MatchTime>2026-10-30 19:00:00</MatchTime>
        <FriendlyType>0</FriendlyType>
        <Opponent><TeamID>654</TeamID><TeamName>FC Pending</TeamName></Opponent>
        <Arena><ArenaID>987</ArenaID><ArenaName>Pending Arena</ArenaName></Arena>
        <Country><CountryID>46</CountryID><CountryName>Switzerland</CountryName></Country>
      </Challenge>
    </ChallengesByMe>
  </Team>
</HattrickData>"""


class FakeSession:
    """Stands in for the OAuth session: records requests, returns canned XML."""

    def __init__(self, responses):
        self.responses = responses
        self.calls = []

    def get(self, url, params):
        self.calls.append((url, params))
        return SimpleNamespace(text=self.responses[params["opponentTeamId"]])


def test_is_challengeable_only_returns_true_ones():
    assert do_challenge.is_challengeable(CHALLENGEABLE_XML) == ["111"]


def test_do_challenge_collects_successes_and_skips_errors():
    session = FakeSession({"111": CHALLENGE_OK_XML, "222": CHALLENGE_ERROR_XML})

    result = do_challenge.do_challenge(
        my_teamid="123", session=session, challengeable_teams=["111", "222"]
    )

    assert result == [
        {
            "team_id": "111",
            "opponent_team_name": "FC Opponent",
            "arena_name": "Opponent Arena",
        }
    ]
    assert len(session.calls) == 2
    url, params = session.calls[0]
    assert url == config.BASE_URL
    assert params["file"] == "challenges"
    assert params["actionType"] == "challenge"
    assert params["teamId"] == "123"
    assert params["opponentTeamId"] == "111"
    # defaults of the public API
    assert params["matchType"] == "1"
    assert params["matchPlace"] == "1"
    assert params["isWeekendFriendly"] == "0"


def test_get_challenges():
    result = do_challenge.get_challenges(CHALLENGES_XML)
    assert result["team_id"] == "123"
    assert result["team_name"] == "FC Test"
    agreed, pending = result["challenges"]
    assert agreed["match_id"] == "1001"
    assert agreed["opponent_team_name"] == "FC Opponent"
    assert agreed["opponent_team_logo"] == "//example.invalid/logo.png"
    assert agreed["country_name"] == "Switzerland"
    assert agreed["is_agreed"] == "True"
    assert pending["match_id"] == ""
    assert pending["opponent_team_logo"] == ""
    assert pending["is_agreed"] == "False"
