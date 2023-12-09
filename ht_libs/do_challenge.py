from bs4 import BeautifulSoup

from . import config



def is_challengeable(challengeable_xml):
	''' 
	Get a list object with challengeable teams
	from challengeable.xml
	'''
	challengeable_teams = []


	challengeable_soup = BeautifulSoup(challengeable_xml, 'xml')


	ChallengeableResult_tag = challengeable_soup.find('ChallengeableResult')


	team_id, *_ = ChallengeableResult_tag.Opponent.TeamId.contents
	is_challengeable, *_ = ChallengeableResult_tag.Opponent.IsChallengeable.contents

	if is_challengeable == 'True':
		challengeable_teams.append(team_id)

	
	return(challengeable_teams)



def do_challenge(session, challengeable_teams):
	''' 
	Takes a list of teams to challenge
	Returns status of challenges as dict
	'''
	challenges = []

	for team_id in challengeable_teams:
		challenge = session.get(config.base_url, params={
			'file': 'challenges',
			'version': '1.6',
			'actionType': 'challenge',
			'teamId':   '',
			'opponentTeamId': team_id,
			'matchType': '1',               # 0 is normal, 1 is cup rules
			'matchPlace': '1',              # 0 is home, 1 is away, 2 is neutral
			'neutralArenaId': '',           # ArenaId for friendly on neutral ground
			})


		challenge_soup = BeautifulSoup(challenge.text, 'xml')


		Error_tag = challenge_soup.find_all('Error')


		if Error_tag is None:
			Opponent_tag = challenge_soup.find('Opponent')
			ArenaName_tag = challenge_soup.find('ArenaName')

			opponent_team_name, *_= Opponent_tag.TeamName.contents
			arena_name, *_ = ArenaName_tag.contents

			challenges = challenges.append({
							'team_id': team_id, 
							'opponent_team_name': opponent_team_name,
							'arena_name': arena_name, 
							})


	return challenges