"""
Python 3.9 
didkit 0.3.0 get_version
"""
import logging
from flask import Flask, render_template, jsonify, request, redirect, Response
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
version = "1.3"


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


# OpenID 
@app.route('/app/issuer/.well-known/openid-configuration', methods=['GET'])
def openid() :
    oidc = {
        'credential_issuer': 'https://app.altme.io/app/issuer',
        'authorization_endpoint':  'https://app.altme.io/app/authorize' 
    }
    return jsonify(oidc)

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
    """ 
    did:web
    
    did:web:app.altme.io:issuer
    
    https://w3c-ccg.github.io/did-method-web/
    https://identity.foundation/.well-known/resources/did-configuration/#LinkedDomains
    """
    # https://tedboy.github.io/flask/generated/generated/flask.Response.html
    headers = { "Content-Type" : "application/did+ld+json",
                "Cache-Control" : "no-cache"
    }
    return Response(json.dumps(did_doc()), headers=headers)


def did_doc() :
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
                        "publicKeyJwk": {
                            "crv":"Ed25519",
                            "kty":"OKP",
                            "x":"FUoLewH4w4-KdaPH2cjZbL--CKYxQRWR05Yd_bIbhQo"
                        }     
                    },
                    {
                        "id": "did:web:app.altme.io:issuer#key-2",
                        "type": "JwsVerificationKey2020",
                        "controller": "did:web:app.altme.io:issuer",
                        "publicKeyJwk": {
                            "kty":"OKP",
                            "crv":"Ed25519",
                            "x":"qrTeh39OTl-xPuYhptNR3nkv0TEjaF4WdWi5Cf5ESs0"
                        }    
                    },
                    {
                        "id": "did:web:app.altme.io:issuer#key-3",
                        "type": "JwsVerificationKey2020",
                        "controller": "did:web:app.altme.io:issuer",
                        "publicKeyJwk": {
                            "crv":"secp256k1",
                            "kty":"EC",
                            "x":"AARiMrLNsRka9wMEoSgMnM7BwPug4x9IqLDwHVU-1A4",
                            "y":"vKMstC3TEN3rVW32COQX002btnU70v6P73PMGcUoZQs",
                        }
                    }
                ],
                "authentication" : [
                    "did:web:app.altme.io:issuer#key-1",
                    "did:web:app.altme.io:issuer#key-2",
                    "did:web:app.altme.io:issuer#key-3"
                ],
                "assertionMethod" : [
                    "did:web:app.altme.io:issuer#key-1",
                    "did:web:app.altme.io:issuer#key-2",
                    "did:web:app.altme.io:issuer#key-3"
                ],
                "keyAgreement" : [
                    "did:web:app.altme.io:issuer#key-2"
                ],
                "capabilityInvocation":[
                    "did:web:app.altme.io:issuer#key-2"
                ]
            }


# MAIN entry point. Flask test server
if __name__ == '__main__':
    app.run(host = mode.IP, port= mode.port, debug=True)
