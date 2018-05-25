#!/usr/bin/env python

from __future__ import print_function
from future import standard_library

standard_library.install_aliases()
import configparser
import sys
import os

import requests
from flask import Flask, request, render_template, abort, jsonify
from multiprocessing import Value

counter = Value('i', 0)
requests.packages.urllib3.disable_warnings()

application = Flask(__name__)

config = configparser.ConfigParser()
config.read('settings.ini')

try:
    post_url = config.get('global', 'posturl')
    ini_category = config.get('global', 'category')
    ini_subcategory = config.get('global', 'subcategory')
    ini_affectedCI = config.get('global','affectedCI')
    verbose = config.get('global','verbose')
    print('Configuration settings:\n\nposturl: %s\ncategory: %s\naffectedCI: %s\nverbose: %s\n\n' % (post_url,ini_category,ini_affectedCI,verbose))

except Exception as ex:
    print('Something is wrong with config: {}'.format(ex))
    sys.exit(1)


@application.route("/")
def hello():
    return 'OK', 200


@application.route("/status")
def status():
    return 'OK\n\n%s events sent\n\nomi server: %s' %(counter.value,post_url)

@application.route("/webhook", methods=['POST'])
def webhook():

    with counter.get_lock():
        counter.value += 1

    if request.method == 'POST':

        alert = request.json
     
        if verbose:
          print("Incoming JSON:\n%s\n" % alert)

        omi = render_template('template.xml',
                              title=alert['commonAnnotations']['summary'],
                              description=alert['commonAnnotations']['description'],
                              severity=alert['commonAnnotations']['severity'],
                              node=alert['commonLabels']['kubernetes_io_hostname'],
                              subcategory=ini_subcategory,
                              category=ini_category,
                              affectedCI=ini_affectedCI
                              )

        if verbose:
          print("Outgoing XML:\n%s\n" % omi)

        headers = {
            'Content-type': 'text/xml',
        }

        if verbose:
          print ("Send to omi %s %s \n%s\n"% (post_url,headers,omi))
        response = requests.post(post_url, headers=headers, data=omi, verify=False)
        return '', response.status_code
    else:
        abort(400)


if __name__ == '__main__':
    application.run(host="0.0.0.0", port=8080)

# port 8080 is needed for s2i in openshift
 
