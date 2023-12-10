from bs4 import BeautifulSoup



def get_my_worlddetails(worlddetails_xml):
    ''' 
    Get a complex dict object with important infos
    for a specific nation from worlddetails.xml
    '''

    world_dict = {}


    world_soup = BeautifulSoup(worlddetails_xml, 'xml')


    LeagueID_tag = world_soup.find('LeagueID')    	
    NumberOfLevels_tag = world_soup.find('NumberOfLevels')

    league_id, *_ = LeagueID_tag.contents
    league_depth, *_ = NumberOfLevels_tag.contents


    world_dict = {	'league_id': league_id, 
                	'league_depth': league_depth,
                	}


    return world_dict
