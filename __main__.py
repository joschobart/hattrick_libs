#!/usr/bin/env python3


""" SAMPLE IMPLEMENTATION FOR ht_libs. """


import json
import sys
from pathlib import Path
from time import sleep

from ht_libs import config, do_hattrick_request, get_matchdetails, get_matches

# from ht_libs import do_challenge
# from ht_libs import get_flags
# from ht_libs import get_matchdetails
# from ht_libs import get_series
# from ht_libs import get_teamdetails
# from ht_libs import get_trainer_avatar


def oauth_reg():
    # # OAuth to hattrick.org
    (
        request_token,
        request_token_secret,
        authorize_url,
    ) = do_hattrick_request.fetch_authorize_url(scope="manage_challenges")

    print(f"Open this URL and authorize Fun with Flags: {authorize_url}")

    sleep(10)

    while True:
        try:
            expression = input("Did you authorize FwF in the browser? (y/n) ")

        except (KeyboardInterrupt, EOFError):
            raise SystemExit()

        if expression.lower() in {"ja", "j", "yes", "y"}:
            try:
                pin = input("Paste the pin from the authorize-website now: ")
                break

            except (KeyboardInterrupt, EOFError):
                raise SystemExit()

        if expression.lower() in {"quit", "exit", "q", "n"}:
            raise SystemExit()

    access_token_key, access_token_secret = do_hattrick_request.get_access_token(
        request_token,
        request_token_secret,
        pin,
    )

    Path("../cache").mkdir(parents=True, exist_ok=True)

    with open("../cache/creds", "x") as f:
        f.write(f"{access_token_key} {access_token_secret}")

    return


def main():
    """
    First we try to oauth with hattrick.org and get the xml-files.
    Second you find some demo-code that shows how to use the libs.
    """
    file = Path("../cache/creds")

    if not file.is_file():
        oauth_reg()

    with open(file, "r") as f:
        line = f.readline()

        creds = []
        for cred in line.split(" "):
            creds.append(cred)

        access_token_key, access_token_secret = creds

    session = do_hattrick_request.open_auth_session(
        access_token_key, access_token_secret
    )

    status = session.get(config.TOKEN_STATUS_URL)

    if status.status_code == 200:
        try:
            # teamdetails_xml = session.get(
            #     config.base_url,
            #     params={
            #         "file": "teamdetails",
            #         "version": "3.6",
            #         "includeFlags": "true",
            #         "userID": "",
            #     },
            # )

            # search_series_xml = session.get(
            #     config.base_url,
            #     params={
            #         "file": "search",
            #         "version": "1.2",
            #         "searchType": "3",
            #         "searchString": "ii.1",
            #         "searchLeagueID": "46",
            #     },
            # )

            # teams_in_series_xml = session.get(
            #     config.base_url,
            #     params={
            #         "file": "leaguedetails",
            #         "version": "1.6",
            #         "leagueLevelUnitID": "8694",
            #     },
            # )

            # challengeable_xml = session.get(
            #     config.BASE_URL,
            #     params={
            #         "file": "challenges",
            #         "version": "1.6",
            #         "actionType": "challengeable",
            #         "teamId": "2101798",
            #         "isWeekendFriendly": "1",
            #         "suggestedTeamIds": "2115616",
            #         "matchType": "1",
            #         "matchPlace": "1",
            #     },
            # )

            # challenges_xml = session.get(
            #     config.base_url,
            #     params={
            #         "file": "challenges",
            #         "version": "1.6",
            #         "actionType": "view",
            #     },
            # )

            # matchdetails_xml = session.get(
            #     config.BASE_URL,
            #     params={
            #         "file": "matchdetails",
            #         "version": "3.1",
            #         "matchEvents": "false",
            #         "matchID": "52282171",
            #         "sourceSystem": "hattrick",
            #     },
            # )

            # staffavatars_xml = session.get(
            #     config.BASE_URL,
            #     params={
            #         "file": "staffavatars",
            #         "version": "1.1",
            #         "teamId": "2101798",
            #     },
            # )

            matches_xml = session.get(
                config.BASE_URL,
                params={
                    "file": "matches",
                    "version": "2.9",
                    "teamID": "",
                },
            )

            print("Download of data successful")
        except Exception as e:
            print(f"{e}: Download of ht-data failed.")
    else:
        print("Problem with oauth-login")

    # # Examples (use of hattrick-api)

    # # Example I:
    # teams_dict = get_flags.get_my_flags(teamdetails_xml.text)
    # print(teams_dict['628463']['flags_home'][0][0])

    # # Example II for a representation like on hattrick:
    # l = []
    # teams_dict = get_flags.get_my_flags(teamdetails_xml.text)

    # for x in range(len(teams_dict['628463']['flags_away'])):
    #     w = str(teams_dict['628463']['flags_away'][x][1])
    #     w = w.lower().replace('ä', 'a')
    #     w = w.replace('ö', 'o').replace('ü', 'u')
    #     l.append((w, (teams_dict['628463']['flags_away'][x][0])))

    # print(sorted(l))

    # # Example III:
    # all_flags = get_flags.get_all_flags()

    # print(json.dumps(all_flags, indent=4).encode('latin1')\
    #                                         .decode('unicode_escape'))

    # Example IV returns missing away flags for team x:
    # all_missing_flags = get_flags.get_missing_flags(teamdetails_xml.text)

    # print(json.dumps(all_missing_flags['628463']['missing_away'], indent=4))

    # Example V returns teamdetails for team x:
    # team_details = get_teamdetails.get_teamdetails(teamdetails_xml.text)

    # print(json.dumps(team_details, indent=4))

    # Example VI returns the series (league) with name x, nation y, teams z:
    # my_series = get_series.get_my_series(search_series_xml.text)
    # my_series_teams = get_series.get_teams_in_series(teams_in_series_xml.text)

    # print(json.dumps(my_series, indent=4))
    # print(json.dumps(my_series_teams, indent=4))

    # Example VII returns a sub-list of challegeable teams and /!\ challenge /!\:
    # my_pot_challenges = do_challenge.is_challengeable(challengeable_xml.text)
    # print(challengeable_xml.text)
    # my_challenges = do_challenge.get_challenges(challenges_xml.text)

    # print(json.dumps(my_pot_challenges, indent=4))

    # my_challenges = do_challenge.do_challenge(session, my_pot_challenges)

    # print(json.dumps(my_pot_challenges, indent=4))
    # print(my_pot_challenges)

    # Example VIII returns the details about match with id x:
    # my_match = get_matchdetails.get_matchdetails(matchdetails_xml.text)

    # print(json.dumps(my_match, indent=4))

    # Example IX returns the details necessary to compile the trainer avatar:
    # my_trainer = get_trainer_avatar.get_trainer_avatar(staffavatars_xml.text)

    # print(json.dumps(my_trainer, indent=4))

    # Example X returns the current list of future and past matches for a team:
    my_matches = get_matches.get_matches(matches_xml.text)

    print(json.dumps(my_matches, indent=4))


if __name__ == "__main__":
    rc = 1

    try:
        main()
        rc = 0
    except Exception as e:
        print("Error: %s" % e, file=sys.stderr)

    sys.exit(rc)
