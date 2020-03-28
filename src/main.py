import flask
import requests
import analyze
from sklearn.linear_model import LogisticRegression as lr
from sklearn import metrics
from sklearn.feature_extraction.text import TfidfVectorizer
import json

# from nltk.corpus import stopwords
import re, string
import numpy as np
from bs4 import BeautifulSoup
import html
from sklearn import preprocessing

import storage

def response(request, response):
    # For more information about CORS and CORS preflight requests, see
    # https://developer.mozilla.org/en-US/docs/Glossary/Preflight_request
    # for more information.

    # Set CORS headers for the preflight request
    if request.method == 'OPTIONS':
        # Allows GET requests from any origin with the Content-Type
        # header and caches preflight response for an 3600s
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600'
        }

        return ('', 204, headers)

    # Set CORS headers for the main request
    headers = {
        'Access-Control-Allow-Origin': '*'
    }

    return (flask.jsonify(response), 200, headers)


def getUserDetails(request):
    user = requests.get('https://randomuser.me/api/').json()
    user = user['results'][0]
    user['generator'] = 'google-cloud-function'
    
    return response(user)

def getJson(request):

    request_json = request.get_json(silent=True)
    request_args = request.args

    if request_json and 'name' in request_json:
        name = request_json['name']
    elif request_args and 'name' in request_args:
        name = request_args['name']
    else:
        name = 'Unknown'

    data = dict(
            name = name,
            text = 'test text'
            )

    return response(request, data)


def sentiment(request):

    request_json = request.get_json(silent=True)
    request_args = request.args

    if request_json and 'text' in request_json:
        text = request_json['text']
    elif request_args and 'text' in request_args:
        text = request_args['text']
    else:
        text = None

    results = analyze.get_sentiment(text)

    return response(request, results)

def topic(request):
    request_json = request.get_json(silent=True)
    request_args = request.args

    if request_json and 'text' in request_json:
        text = request_json['text']
    elif request_args and 'text' in request_args:
        text = request_args['text']
    else:
        text = None

    results = analyze.get_topic(text)

    return response(request, results)

def transform(text, vect = None):

    if vect == None:
        vect = TfidfVectorizer(max_features=2000, ngram_range=(1,3))
        vect.fit(text)

    text = vect.transform(text)

    return text, vect


def labelEncoder(y):
    le = preprocessing.LabelEncoder()
    le.fit(y)

    # print('>> classes', list(le.classes_))

    return (le.transform(y), len(le.classes_), le.classes_)

def fit(text, targets, classifier = lr, params = dict(C=1000, penalty='l2', solver='liblinear', multi_class='auto')):

    # get texts, verify shape
    # get targets, verify if target contain only one column

    # set model and parameters

    classifier.fit(text, targets)

    return classifier

def clean(doc):

    # Lowercase
    doc = doc.lower()
    # Remove HTML codes
    try:
        doc = BeautifulSoup(doc, features="lxml").get_text()
    except:
        pass
    # Remove numbers
    # doc = re.sub(r"[0-9]+", "", doc)
    # remove HTML space code
    # tokens = tokens.replace('&nbsp', string.whitespace)
    # Split in tokens
    tokens = doc.split(" ")
    # Remove punctuation
    # tokens = [w.translate(str.maketrans('', '', string.punctuation)) for w in tokens]
    # remove html codes
    tokens = [html.unescape(w) for w in tokens]

    # Tokens with less then two characters will be ignored
    tokens = [word for word in tokens if len(word) > 1]

    return ' '.join(tokens)

def train_model(text, targets):

    text, vect = transform(text)
    targets, n_classes, classes_name = labelEncoder(targets)

    # targets labels
    model = fit(text, targets)
    # model.save to firestore
    return 0

def test_model(text):

    # load vect from firestore
    text, vect = transform(text)

    # load model from firestore
    pred = model.predict_proba(text)

    return pred

# STORAGE

def update_object(filename, content):
    return storage.upload_object('metatext-models', filename, content, readers=[], owners=[])

import googleapiclient.discovery
import googleapiclient.http

import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="./credentials/API-project-credentials.json"


# Converts strings added to /messages/{pushId}/original to uppercase
def leads(data, context):
    send_email(data)

import smtplib

def send_email(content = 'test'):
    gmail_user = 'rafaelsandronidias@gmail.com'
    gmail_password = 'sndrn@gmail09!'

    sent_from = gmail_user
    to = ['rafaelsandronidias@gmail.com']
    subject = 'MetaText New lead'
    body = json.dumps(content)

    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (sent_from, ", ".join(to), subject, body)

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(sent_from, to, message)
        server.close()

        print('Email sent!')
    except:
        print('Something went wrong...')

if __name__ == '__main__':

    send_email()
