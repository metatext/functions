#!/usr/bin/env python

# Copyright 2016 Google, Inc
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Analyzes text using the Google Cloud Natural Language API."""

import argparse
import json
import sys

import googleapiclient.discovery

import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="./credentials/API-project-credentials.json"


def get_native_encoding_type():
    """Returns the encoding type that matches Python's native strings."""
    if sys.maxunicode == 65535:
        return 'UTF16'
    else:
        return 'UTF32'


def analyze_entities(text, encoding='UTF32'):
    body = {
        'document': {
            'type': 'PLAIN_TEXT',
            'content': text,
        },
        # 'encoding_type': encoding,
    }

    service = googleapiclient.discovery.build('language', 'v1')

    # request = service.documents().analyzeEntities(body=body)
    request = service.documents().classifyText(body=body)

    response = request.execute()

    return response


def analyze_sentiment(text, encoding='UTF32'):
    body = {
        'document': {
            'type': 'PLAIN_TEXT',
            'content': text,
        },
        'encoding_type': encoding
    }

    service = googleapiclient.discovery.build('language', 'v1')

    request = service.documents().analyzeSentiment(body=body)
    response = request.execute()

    return response


def analyze_syntax(text, encoding='UTF32'):
    body = {
        'document': {
            'type': 'PLAIN_TEXT',
            'content': text,
        },
        'encoding_type': encoding
    }

    service = googleapiclient.discovery.build('language', 'v1')

    request = service.documents().analyzeSyntax(body=body)
    response = request.execute()

    return response


def get_topic(text):
    if text == None: return dict(topic = '', confidence = 0)

    result = analyze_entities(text, get_native_encoding_type())
    
    arr = []
    for r in result['categories']:
        arr.append( dict(
            topic = str(r['name']).replace("/",""),
            confidence = r['confidence']
            ))

    return arr

def get_sentiment(text):
    
    """
    if args.command == 'entities':
        result = analyze_entities(args.text, get_native_encoding_type())
    elif args.command == 'sentiment':
        result = analyze_sentiment(args.text, get_native_encoding_type())
    elif args.command == 'syntax':
        result = analyze_syntax(args.text, get_native_encoding_type())
    """
    if text == None: return dict(score = 0)

    result = analyze_sentiment(text, get_native_encoding_type())

    sentiment = result['documentSentiment']

    language = result['language']

    """
    sentiment_results = dict(
        positive = ["score": 0.8, "magnitude": 3.0]
        negative = ["score": -0.6, "magnitude": 4.0]
        neutral  = ["score": 0.1, "magnitude": 0.0]
        mixed    = ["score": 0.0, "magnitude": 4.0]
        )
    """
    # sentiment results
    score = sentiment['score']
    magnitude = sentiment['magnitude']
    if score > 0:
        tag = 'positive'
    elif score < 0:
        tag = 'negative'
    elif score == 0 and magnitude > 0:
        tag = 'mixed'
    else:
        tag = 'neutral'

    sentiment_results = dict(
        language = language,
        score = score,
        tag = tag,
        magnitude = magnitude
        )

    return sentiment_results

"""
if __name__ == '__main__':
    text = 'By looking at labeled data our software can learn new objects and patterns. Of course, it only identifies objects it has learned about.'
    get_entities(text)
"""
