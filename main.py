"""
Python 3.9 
didkit 0.3.0 get_version
"""
import logging
from flask import Flask, render_template, jsonify, request, redirect
import json
import environment
import os
import sys
from device_detector import SoftwareDetector

logging.basicConfig(level=logging.INFO)

logging.info("python version : %s", sys.version)

# init
myenv = os.getenv('MYENV')
if not myenv :
   myenv='local'
mode = environment.currentMode(myenv)
app = Flask(__name__)
app.jinja_env.globals['Version'] = "0.7.1"
app.config['SESSION_PERMANENT'] = True
app.config['SESSION_COOKIE_NAME'] = 'altme'
app.config['SESSION_TYPE'] = 'redis' # Redis server side session
app.config['SESSION_FILE_THRESHOLD'] = 100
app.config['SECRET_KEY'] = "altme_app"

version = "1.1"

issuer_key = json.load(open("keys.json", "r"))['talao_Ed25519_private_key']
issuer_did = "did:tz:tz1NyjrTUNxDpPaqNZ84ipGELAcTWYg6s5Du"
issuer_vm = "did:tz:tz1NyjrTUNxDpPaqNZ84ipGELAcTWYg6s5Du#blockchainAccountId"


@app.route('/login' , methods=['GET']) 
@app.route('/' , methods=['GET']) 
def test() :
   return jsonify("hello , version : " + version)


@app.route('/device_detector' , methods=['GET']) 
def device_detector ():
    ua = request.headers.get('User-Agent')
    device = SoftwareDetector(ua).parse()
    logging.info(device.os_name())
    if device.os_name() == "Android" :
        return redirect("https://play.google.com/store/apps/details?id=co.altme.alt.me.altme")
    elif device.os_name() == "iOS" : 
        return redirect("https://apps.apple.com/fr/app/altme/id1633216869")
    else :
        return jsonify('unknown device')    


# Google universal link
@app.route('/.well-known/assetlinks.json' , methods=['GET']) 
def assetlinks(): 
    document = json.load(open('assetlinks.json', 'r'))
    return jsonify(document)


# Apple universal link
@app.route('/.well-known/apple-app-site-association' , methods=['GET']) 
def apple_app_site_association(): 
    document = json.load(open('apple-app-site-association', 'r'))
    return jsonify(document)


@app.route('/app/download' , methods=['GET']) 
def app_download() :
    return render_template('app_download.html')


# .well-known DID API
@app.route('/issuer/.well-known/did.json', methods=['GET'])
@app.route('/issuer/did.json', methods=['GET'])
def well_known_did () :
    """ did:web
    https://w3c-ccg.github.io/did-method-web/
    https://identity.foundation/.well-known/resources/did-configuration/#LinkedDomains
    """
    del issuer_key['d']
    DidDocument = did_doc(issuer_key)
    return jsonify(DidDocument)


def did_doc(issuer_key) :
    return  {
                "@context": [
                    "https://www.w3.org/ns/did/v1",
                    {
                        "@id": "https://w3id.org/security#publicKeyJwk",
                        "@type": "@json"
                    }
                ],
                "id": "did:web:app.altme.io:issuer",
                "verificationMethod": [
                    {
                        "id": "did:web:app.altme.io:issuer#key-1",
                        "type": "JwsVerificationKey2020",
                        "controller": "did:web:app.altme.io:issuer",
                        "publicKeyJwk": issuer_key     
                    },
                ],
                "authentication" : [
                    "did:web:app.altme.io:issuer#key-1",
                ],
                "assertionMethod" : [
                    "did:web:app.altme.io:issuer#key-1",
                ],
                "keyAgreement" : [
                    "did:web:app.altme.io:issuer#key-1"
                ],
                "capabilityInvocation":[
                    "did:web:app.altme.io:issuer#key-1"
                ]
            }


# MAIN entry point. Flask test server
if __name__ == '__main__':
    app.run(host = mode.IP, port= mode.port, debug=True)
