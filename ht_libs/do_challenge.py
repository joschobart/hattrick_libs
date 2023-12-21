from bs4 import BeautifulSoup

from . import config



def is_challengeable(challengeable_xml):
	''' 
	Get a list object with challengeable teams
	from challengeable.xml
	'''
	challengeable_teams = []


	challengeable_soup = BeautifulSoup(challengeable_xml, 'xml')


	Opponent_tags = challengeable_soup.find_all('Opponent')


	for Opponent_tag in Opponent_tags:
		try:
			team_id, *_ = Opponent_tag.TeamId.contents
		except:
			team_id = None

		try:
			is_challengeable, *_ = Opponent_tag.IsChallengeable.contents
		except:
			is_challengeable = 'False'


		if is_challengeable == 'True':
			challengeable_teams.append(team_id)


	return(challengeable_teams)



def do_challenge(my_teamid, session, challengeable_teams):
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
			'teamId':   my_teamid,
			'opponentTeamId': team_id,
			'matchType': '1',               # 0 is normal, 1 is cup rules
			'matchPlace': '1',              # 0 is home, 1 is away, 2 is neutral
			'neutralArenaId': '',           # ArenaId for friendly on neutral ground
			})


		challenge_soup = BeautifulSoup(challenge.text, 'xml')


		Error_tag = challenge_soup.find_all('Error')


		print(type(Error_tag))


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

	print(challenges)

	return challenges



def get_challenges(challenges_xml):
	''' 
	Get a dict object with challenged teams
	from challenges.xml
	'''
	challenges = []


	challenged_teams_soup = BeautifulSoup(challenges_xml, 'xml')


	Team_tag = challenged_teams_soup.find('Team')

	team_id, *_ = Team_tag.TeamID.contents
	team_name, *_ = Team_tag.TeamName.contents


	try:
		Challenge_tags = challenged_teams_soup.find_all('Challenge')

	except:
		challenges = None


	print(Challenge_tags)

	else:
		for Challenge_tag in Challenge_tags:

			training_match_id, *_ = Challenge_tag.TrainingMatchID.contents
			match_id, *_ = Challenge_tag.MatchID.contents
			match_time, *_ = Challenge_tag.MatchTime.contents
			friendly_type, *_ = Challenge_tag.FriendlyType.contents
			opponent_team_id, *_ = Challenge_tag.Opponent.TeamID.contents
			opponent_team_name, *_ = Challenge_tag.Opponent.TeamName.contents

			try:
				opponent_team_logo, *_ = Challenge_tag.Opponent.LogoURL.contents
			except:
				opponent_team_logo = ''

			arena_id, *_ = Challenge_tag.Arena.ArenaID.contents
			arena_name, *_ = Challenge_tag.Arena.ArenaName.contents
			country_id, *_ = Challenge_tag.Country.CountryID.contents
			country_name, *_ = Challenge_tag.Country.CountryName.contents

			try:
				is_agreed, *_ = Challenge_tag.IsAgreed.contents
			except:
				is_agreed = 'False'


			challenges = { 	'team_id': team_id,
							'team_name': team_name,
							'training_match_id': training_match_id,
							'match_id': match_id,
							'match_time': match_time,
							'friendly_type': friendly_type,
							'opponent_team_id': opponent_team_id,
							'opponent_team_name': opponent_team_name,
							'opponent_team_logo': opponent_team_logo,
							'arena_id': arena_id,
							'arena_name': arena_name, 
							'country_id': country_id,
							'country_name': country_name, 
							'is_agreed': is_agreed, 
							}


	return challenges







# <?xml version="1.0" encoding="utf-8"?>
# <HattrickData>
#   <FileName>challenges.xml</FileName>
#   <Version>1.6</Version>
#   <UserID>9034788</UserID>
#   <FetchedDate>2023-12-15 23:47:57</FetchedDate>
#   <Team>
#     <TeamID>2101798</TeamID>
#     <TeamName>Les Béliers Anarchistes</TeamName>
#     <ChallengesByMe>
#       <Challenge>
#         <TrainingMatchID>76683104</TrainingMatchID>
#         <MatchID>725189167</MatchID>
#         <MatchTime>2023-12-20 20:50:00</MatchTime>
#         <FriendlyType>1</FriendlyType>
#         <Opponent>
#           <TeamID>1667897</TeamID>
#           <TeamName>Tristan Kickers</TeamName>
#           <LogoURL></LogoURL>
#         </Opponent>
#         <Arena>
#           <ArenaID>1664459</ArenaID>
#           <ArenaName>Tristan Kickers Arena</ArenaName>
#         </Arena>
#         <Country>
#           <CountryID>72</CountryID>
#           <CountryName>Morocco</CountryName>
#         </Country>
#         <IsAgreed>True</IsAgreed>
#       </Challenge>
#     </ChallengesByMe>
#     <OffersByOthers />
#   </Team>
# </HattrickData>


# <?xml version="1.0" encoding="utf-8"?>
# <HattrickData>
#   <FileName>challenges.xml</FileName>
#   <Version>1.6</Version>
#   <UserID>9034788</UserID>
#   <FetchedDate>2023-12-15 23:41:15</FetchedDate>
#   <Team>
#     <TeamID>628463</TeamID>
#     <TeamName>Galatasaray Isstmalcool</TeamName>
#     <ChallengesByMe>
#       <Challenge>
#         <TrainingMatchID>76687570</TrainingMatchID>
#         <MatchTime>2023-12-20 20:50:00</MatchTime>
#         <FriendlyType>1</FriendlyType>
#         <Opponent>
#           <TeamID>2014806</TeamID>
#           <TeamName>Sidi Ifni FC</TeamName>
#           <LogoURL>http://res.hattrick.org/teamlogo/21/202/2015/2014806/2014806.png</LogoURL>
#         </Opponent>
#         <Arena>
#           <ArenaID>2011367</ArenaID>
#           <ArenaName>Sidi Ifni FC Arena</ArenaName>
#         </Arena>
#         <Country>
#           <CountryID>72</CountryID>
#           <CountryName>Morocco</CountryName>
#         </Country>
#         <IsAgreed>False</IsAgreed>
#       </Challenge>
#       <Challenge>
#         <TrainingMatchID>76687569</TrainingMatchID>
#         <MatchTime>2023-12-20 20:50:00</MatchTime>
#         <FriendlyType>1</FriendlyType>
#         <Opponent>
#           <TeamID>2014563</TeamID>
#           <TeamName>Bédouins Grolandais Affiliés</TeamName>
#           <LogoURL>http://res.hattrick.org/teamlogo/21/202/2015/2014563/2014563.png</LogoURL>
#         </Opponent>
#         <Arena>
#           <ArenaID>2011124</ArenaID>
#           <ArenaName>Fond du Trou</ArenaName>
#         </Arena>
#         <Country>
#           <CountryID>72</CountryID>
#           <CountryName>Morocco</CountryName>
#         </Country>
#         <IsAgreed>False</IsAgreed>
#       </Challenge>
#       <Challenge>
#         <TrainingMatchID>76687568</TrainingMatchID>
#         <MatchTime>2023-12-20 20:50:00</MatchTime>
#         <FriendlyType>1</FriendlyType>
#         <Opponent>
#           <TeamID>2016192</TeamID>
#           <TeamName>Atlas MTP84</TeamName>
#           <LogoURL>https://imgur.com/mB43Zbs.png</LogoURL>
#         </Opponent>
#         <Arena>
#           <ArenaID>2012753</ArenaID>
#           <ArenaName>Vélodrome</ArenaName>
#         </Arena>
#         <Country>
#           <CountryID>72</CountryID>
#           <CountryName>Morocco</CountryName>
#         </Country>
#         <IsAgreed>False</IsAgreed>
#       </Challenge>
#       <Challenge>
#         <TrainingMatchID>76687577</TrainingMatchID>
#         <MatchTime>2023-12-20 20:50:00</MatchTime>
#         <FriendlyType>1</FriendlyType>
#         <Opponent>
#           <TeamID>1668216</TeamID>
#           <TeamName>moutfiboys23</TeamName>
#           <LogoURL></LogoURL>
#         </Opponent>
#         <Arena>
#           <ArenaID>1664778</ArenaID>
#           <ArenaName>moutfiboys23</ArenaName>
#         </Arena>
#         <Country>
#           <CountryID>72</CountryID>
#           <CountryName>Morocco</CountryName>
#         </Country>
#         <IsAgreed>False</IsAgreed>
#       </Challenge>
#       <Challenge>
#         <TrainingMatchID>76687578</TrainingMatchID>
#         <MatchTime>2023-12-20 20:50:00</MatchTime>
#         <FriendlyType>1</FriendlyType>
#         <Opponent>
#           <TeamID>1668172</TeamID>
#           <TeamName>moutfi reserve</TeamName>
#           <LogoURL></LogoURL>
#         </Opponent>
#         <Arena>
#           <ArenaID>1664734</ArenaID>
#           <ArenaName>moutfi reserve Arena</ArenaName>
#         </Arena>
#         <Country>
#           <CountryID>72</CountryID>
#           <CountryName>Morocco</CountryName>
#         </Country>
#         <IsAgreed>False</IsAgreed>
#       </Challenge>
#       <Challenge>
#         <TrainingMatchID>76687571</TrainingMatchID>
#         <MatchTime>2023-12-20 20:50:00</MatchTime>
#         <FriendlyType>1</FriendlyType>
#         <Opponent>
#           <TeamID>2015708</TeamID>
#           <TeamName>Rajaa Club Athletic Maroc</TeamName>
#           <LogoURL>http://res.hattrick.org/teamlogo/21/202/2016/2015708/2015708.png</LogoURL>
#         </Opponent>
#         <Arena>
#           <ArenaID>2012269</ArenaID>
#           <ArenaName>Rajaa Club Athletic  Arena</ArenaName>
#         </Arena>
#         <Country>
#           <CountryID>72</CountryID>
#           <CountryName>Morocco</CountryName>
#         </Country>
#         <IsAgreed>False</IsAgreed>
#       </Challenge>
#       <Challenge>
#         <TrainingMatchID>76687573</TrainingMatchID>
#         <MatchTime>2023-12-20 20:50:00</MatchTime>
#         <FriendlyType>1</FriendlyType>
#         <Opponent>
#           <TeamID>2015417</TeamID>
#           <TeamName>Chefchaouen FC</TeamName>
#           <LogoURL>//res.hattrick.org/teamlogo/21/202/2016/2015417/2015417.jpg</LogoURL>
#         </Opponent>
#         <Arena>
#           <ArenaID>2011978</ArenaID>
#           <ArenaName>GLOIRE AU MDJ ARENA</ArenaName>
#         </Arena>
#         <Country>
#           <CountryID>72</CountryID>
#           <CountryName>Morocco</CountryName>
#         </Country>
#         <IsAgreed>False</IsAgreed>
#       </Challenge>
#       <Challenge>
#         <TrainingMatchID>76687574</TrainingMatchID>
#         <MatchTime>2023-12-20 20:50:00</MatchTime>
#         <FriendlyType>1</FriendlyType>
#         <Opponent>
#           <TeamID>2014248</TeamID>
#           <TeamName>CasablancaZürich</TeamName>
#           <LogoURL>http://res.hattrick.org/teamlogo/21/202/2015/2014248/2014248.png</LogoURL>
#         </Opponent>
#         <Arena>
#           <ArenaID>2010809</ArenaID>
#           <ArenaName>CasablancaZürich Arena</ArenaName>
#         </Arena>
#         <Country>
#           <CountryID>72</CountryID>
#           <CountryName>Morocco</CountryName>
#         </Country>
#         <IsAgreed>False</IsAgreed>
#       </Challenge>
#       <Challenge>
#         <TrainingMatchID>76687572</TrainingMatchID>
#         <MatchTime>2023-12-20 20:50:00</MatchTime>
#         <FriendlyType>1</FriendlyType>
#         <Opponent>
#           <TeamID>1668031</TeamID>
#           <TeamName>Toubkal</TeamName>
#           <LogoURL>//res.hattrick.org/teamlogo/17/167/1669/1668031/1668031.png</LogoURL>
#         </Opponent>
#         <Arena>
#           <ArenaID>1664593</ArenaID>
#           <ArenaName>Toubkal Arena</ArenaName>
#         </Arena>
#         <Country>
#           <CountryID>72</CountryID>
#           <CountryName>Morocco</CountryName>
#         </Country>
#         <IsAgreed>False</IsAgreed>
#       </Challenge>
#       <Challenge>
#         <TrainingMatchID>76687576</TrainingMatchID>
#         <MatchTime>2023-12-20 20:50:00</MatchTime>
#         <FriendlyType>1</FriendlyType>
#         <Opponent>
#           <TeamID>1667848</TeamID>
#           <TeamName>Mackems AFC</TeamName>
#           <LogoURL></LogoURL>
#         </Opponent>
#         <Arena>
#           <ArenaID>1664410</ArenaID>
#           <ArenaName>Mackems AFC Arena</ArenaName>
#         </Arena>
#         <Country>
#           <CountryID>72</CountryID>
#           <CountryName>Morocco</CountryName>
#         </Country>
#         <IsAgreed>False</IsAgreed>
#       </Challenge>
#       <Challenge>
#         <TrainingMatchID>76687575</TrainingMatchID>
#         <MatchTime>2023-12-20 20:50:00</MatchTime>
#         <FriendlyType>1</FriendlyType>
#         <Opponent>
#           <TeamID>282873</TeamID>
#           <TeamName>Chamakh All Star</TeamName>
#           <LogoURL>//res.hattrick.org/teamlogo/3/29/283/282873/282873.jpg</LogoURL>
#         </Opponent>
#         <Arena>
#           <ArenaID>282873</ArenaID>
#           <ArenaName>Stade Hicham El Guerrouj</ArenaName>
#         </Arena>
#         <Country>
#           <CountryID>72</CountryID>
#           <CountryName>Morocco</CountryName>
#         </Country>
#         <IsAgreed>False</IsAgreed>
#       </Challenge>
#     </ChallengesByMe>
#     <OffersByOthers />
#   </Team>
# </HattrickData>
