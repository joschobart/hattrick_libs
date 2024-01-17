""" Functions to get the trainer-avatar-image from staffavatars.xml. """


from bs4 import BeautifulSoup


def get_trainer_avatar(staffavatars_xml):
    """
    Get a complex dict object to render the trainer
    avatar from staffavatars.xml
    """
    trainer_avatar_dict = {}

    trainer_avatar_soup = BeautifulSoup(staffavatars_xml, "xml")

    Trainer_tag = trainer_avatar_soup.find("Trainer")

    Layer_tags = Trainer_tag.Avatar.find_all("Layer")

    trainer_id, *_ = Trainer_tag.TrainerId.contents

    trainer_avatar_dict["trainer_id"] = trainer_id

    _tuples = [
        ("backgrounds", "avatar_background"),
        ("bodies", "avatar_body"),
        ("faces", "avatar_face"),
        ("eyes", "avatar_eyes"),
        ("mouths", "avatar_mouth"),
        ("noses", "avatar_nose"),
        ("hair", "avatar_hair"),
    ]

    for Layer_tag in Layer_tags:
        for _tuple in _tuples:
            if str(Layer_tag.Image.contents).find(_tuple[0]) != -1:
                _x = int(Layer_tag.get("x")) - 4
                _y = int(Layer_tag.get("y")) - 5
                _url = Layer_tag.Image.contents[0]
                trainer_avatar_dict[_tuple[1]] = {
                    "left": f"{_x}px",
                    "top": f"{_y}px",
                    "url": _url,
                }

    return trainer_avatar_dict
