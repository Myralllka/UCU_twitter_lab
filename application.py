#!/bin/env python3

import urllib.request
import urllib.parse
import urllib.error
from docs import twurl
import ssl
import json
import sys
import os


# https://apps.twitter.com/
# Create App and get the four strings, put them in hidden.py


def input_account():
    """
    function to read account name
    :return: account_name if it is not empty, else exit from the application
    """
    account_name = input('Enter Twitter Account:')
    if account_name:
        return account_name
    sys.exit()


def initial():
    """
    function to create a tmp json file with information from twitter
    """
    account_name = input_account()
    url = twurl.augment(TWITTER_URL, {'screen_name': account_name})
    connection = urllib.request.urlopen(url, context=ctx)
    # headers = dict(connection.getheaders())
    # print('Remaining', headers['x-rate-limit-remaining'])
    data = connection.read().decode()
    with open('./tmp/data.json', 'w') as out_file:
        print(data, file=out_file)


def main_json_travel():
    """
    main function to move up in .json file
    :return: 0 if program finished without errors, -1 if any error occurred
    """
    with open('./tmp/data.json', encoding='utf-8') as ff:
        data = json.load(fp=ff)
    current = data
    while True:
        try:
            if type(current) == dict:
                print(' | '.join(list(i for i in current)))
                current = eval('current' + '[\'' +
                               input('direction: ') + '\']')
            elif type(current) == list:
                print(' | '.join(list(i['name'] for i in current)))
                path, c = input('direction: '), 0
                for i in range(len(current)):
                    if current[i]['name'] == path:
                        c = i
                        break
                current = eval('current' + '[' + str(c) + ']')
            else:
                print(current)
                return 0
        except KeyError:
            print('Your input was incorrect!')
            return -1


if __name__ == "__main__":
    # Ignore SSL certificate errors
    TWITTER_URL = 'https://api.twitter.com/1.1/friends/list.json'
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    initial()
    main_json_travel()
    question = input('Do you want to delete the file? (Y/n)')
    if question == 'n':
        sys.exit()
    os.system('rm ./tmp/data.json')
