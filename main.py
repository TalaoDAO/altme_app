"""
Python 3.9 
didkit 0.3.0 get_version
"""
from flask import Flask, render_template, jsonify
import json
import environment
import os
import sys


print("python version : ", sys.version)

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

version = "1.0"

@app.route('/login' , methods=['GET']) 
@app.route('/' , methods=['GET']) 
def test() :
   return jsonify("hello , version : " + version)


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


# MAIN entry point. Flask test server
if __name__ == '__main__':
    app.run(host = mode.IP, port= mode.port, debug=True)
