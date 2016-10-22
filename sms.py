#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import os, sys, requests, ConfigParser

def eprint(*args, **kwargs):

    print(*args, file=sys.stderr, **kwargs)

def main():

    config = ConfigParser.ConfigParser()
    config.read(os.path.expanduser('~/.sms.py.conf'))

    user = config.get('auth', 'user')
    password = config.get('auth', 'password')

    url = config.get('service', 'url')

    text = sys.stdin.read()

    params = { "user": user, "pass": password, "msg": text.strip() }

    r = requests.get(url, params)

    if r.status_code == 400:
        eprint("Un des paramètres obligatoires est manquant (code %i)" % r.status_code)
    elif r.status_code == 402:
        eprint("Trop de SMS ont été envoyés en trop peu de temps (code %i)" % r.status_code)
    elif r.status_code == 403:
        eprint("Le service n'est pas activé sur l'espace abonné, ou login / clé incorrect (code %i)" % r.status_code)
    elif r.status_code == 500:
        eprint("Erreur côté serveur. Veuillez réessayez ultérieurement (code %i)" % r.status_code)

    if r.status_code != 200:
        sys.exit(1)

if __name__ == '__main__':
    try:
        main()
        sys.exit(0)
    except KeyboardInterrupt, SystemExit:
        pass
