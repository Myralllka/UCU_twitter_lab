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
    main function to move the in .json file
    :return: 0 if program finished without errors, -1 if any error occurred
    """
    with open('./tmp/data.json', encoding='utf-8') as ff:
        data = json.load(fp=ff)
    path_dict, path_line = dict(), 'current',
    path_dict[path_line], current, line = data, data, path_line
    while True:
        try:
            # print possible directories to move
            if type(current) == dict:
                print(' | '.join(list(i for i in current)))
            elif type(current) == list:
                print(' | '.join(list(str(i) for i in range(len(current)))))
            else:
                print('\n' + '-' * 5 + 'EOF' + '-' * 5)
            input_path = input('print here direction (qq to come back): ')
            # move back the tree
            if input_path == 'qq':
                path_line = ''.join(list(path_line)[:path_line.rindex('[')])
                current = path_dict[path_line]
                continue
            # try to move up the tree
            try:
                current = eval(line + '[\'' + input_path + '\']')
                path_line += '[\'' + input_path + '\']'
                path_dict[path_line] = current
            except TypeError:
                current = eval(line + '[' + input_path + ']')
                path_line += '[' + input_path + ']'
                path_dict[path_line] = current
        except KeyError:
            print('Your input was incorrect!')
            continue
        except KeyboardInterrupt:
            sys.exit()
        except:
            print('YOU DID SOMETHING WRONG. TRY ONE MORE TIME')
            continue


if __name__ == "__main__":
    # Ignore SSL certificate errors
    TWITTER_URL = 'https://api.twitter.com/1.1/friends/list.json'
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    initial()
    print("(Ctrl+C to exit)")
    main_json_travel()
    question = input('Do you want to delete the file? (Y/n)')
    if question == 'n':
        sys.exit()
    os.system('rm ./tmp/data.json')
