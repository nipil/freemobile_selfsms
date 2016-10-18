#! /usr/bin/env python

import os, sys, requests, ConfigParser

if __name__ == '__main__':

    config = ConfigParser.ConfigParser()
    config.read(os.path.expanduser('~/.sms.py.conf'))

    user = config.get('auth', 'user')
    password = config.get('auth', 'password')

    url = config.get('service', 'url')

    text = sys.stdin.read()

    params = { "user": user, "pass": password, "msg": text.strip() }

    r = requests.get(url, params)
    if r.status_code != 200:
	print r.status_code

