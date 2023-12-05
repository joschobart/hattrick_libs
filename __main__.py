#!/usr/bin/env python3



### EXAMPLE-IMPLEMENTATION ###



import sys
import json

from time import sleep
from pathlib import Path

from ht_libs import do_hattrick_request
from ht_libs import get_teamdetails
from ht_libs import get_flags



def oauth_reg():
    # # OAuth to hattrick.org
    request_token, request_token_secret, authorize_url = \
        do_hattrick_request.fetch_authorize_url(scope='manage_challenges')

    print(f'Open this URL and authorize Fun with Flags: {authorize_url}')

    sleep(10)


    while True:

        try:
            expression = input(f'Did you authorize FwF in the browser? (y/n) ')

        except (KeyboardInterrupt, EOFError):
            raise SystemExit()

        if expression.lower() in {'ja', 'j', 'yes', 'y'}:
            try:
                pin = input(f'Paste the pin from the authorize-website now: ')
                break

            except (KeyboardInterrupt, EOFError):
                raise SystemExit()


        if expression.lower() in {'quit', 'exit', 'q', 'n'}:
            raise SystemExit()


        try:
            result = evaluate(expression)

        except SyntaxError:
            print("Invalid input expression syntax")
            continue


    access_token_key, access_token_secret = do_hattrick_request.get_access_token(
        request_token,
        request_token_secret,
        pin,
        )

    Path('../cache').mkdir(parents=True, exist_ok=True)

    with open('../cache/creds', 'x') as f:
         f.write(f'{access_token_key} {access_token_secret}')

    return



def main():
    '''
    First we try to oauth with hattrick.org and get the xml-files.
    Second you find some demo-code that shows how to use the libs.
    '''


    session_status_url = 'https://chpp.hattrick.org/oauth/check_token.ashx'
    api_url = 'https://chpp.hattrick.org/chppxml.ashx'
    file = Path('../cache/creds')


    if not file.is_file():
        oauth_reg()
    

    with open(file, 'r') as f:
        line = f.readline()

        creds = []
        for cred in line.split(' '):
            creds.append(cred)

        access_token_key, access_token_secret = creds


    session = do_hattrick_request.open_auth_session(access_token_key, access_token_secret)

    status = session.get(session_status_url)


    if status.status_code == 200:
        try:
            teamdetails_xml = session.get(api_url, params={
                'file': 'teamdetails', 
                'version': '3.6',
                'includeFlags': 'true',
                })

            print('Download of data successful')
        except:
            print('Problem downloading fresh data')
    else:
        print('Problem with oauth-login')



    # # Examples (use hattrick-api)


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

    # print(len(all_flags))


    # Example IV shows missing away flags for team x:
    all_missing_flags = get_flags.get_missing_flags(teamdetails_xml.text)

    print(json.dumps(all_missing_flags['628463']['missing_away'], indent=4))


    # Example V shows teamdetails for team x:
    # team_details = get_teamdetails.get_my_teamdetails(teamdetails_xml.text)

    # print(json.dumps(team_details, indent=4))



if __name__ == '__main__':
    rc = 1

    try:
        main()
        rc = 0
    except Exception as e:
        print('Error: %s' % e, file=sys.stderr)

    sys.exit(rc)
