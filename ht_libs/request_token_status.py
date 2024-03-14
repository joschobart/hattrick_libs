""" Function to get data about the actual oauth token. """


from bs4 import BeautifulSoup


def request_token_status(token_status_xml):
    """
    Get a dict object about the used token
    """
    token_soup = BeautifulSoup(token_status_xml, "xml")

    UserID_tag = token_soup.find("UserID")

    user_id = UserID_tag.contents

    token_dict = {
        "user_id": user_id,
    }

    return token_dict
