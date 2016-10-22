#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import os, sys, requests, ConfigParser, argparse, logging

def eprint(*args, **kwargs):

    print(*args, file=sys.stderr, **kwargs)

def activate_debug():

    # These two lines enable debugging at httplib level (requests->urllib3->http.client)
    # You will see the REQUEST, including HEADERS and DATA, and RESPONSE with HEADERS but without DATA.
    # The only thing missing will be the response.body which is not logged.
    try:
        import http.client as http_client
    except ImportError:
        # Python 2
        import httplib as http_client
    http_client.HTTPConnection.debuglevel = 1

    # You must initialize logging, otherwise you'll not see debug output.
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(logging.DEBUG)
    requests_log.propagate = True

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--log', help='choix du niveau de log', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL', 'EXCEPTION'], default='WARNING')
    return parser.parse_args()

def main():

    args = parse_arguments()

    if args.log == 'DEBUG':
        activate_debug()

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
