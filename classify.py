import argparse
import io
import json
import os

import googleapiclient.discovery
from google.cloud import language
import numpy
import six

# Google API Credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="./credentials/API-project-credentials.json"

#
def transformer(text):
    return []

def classify_train(model_id=None, text, labels):
    result = []
    # transformer

    # return accuracy and f1score from trained model
    return result


def classify_test(model_id=None, input):
    """ 
    Classify the input text into categories. 

    model_id: int - model identifier
    input: array - texts to be predicted
    return: array - predicted labels by order
    """

    # transform text into bag of words / tfidf
    # load trained model from database

    # picker.loads()

    #

    language_client = language.LanguageServiceClient()

    document = language.types.Document(
        content=text,
        type=language.enums.Document.Type.PLAIN_TEXT)
    response = language_client.classify_text(document)
    categories = response.categories

    result = {}

    for category in categories:
        # Turn the categories into a dictionary of the form:
        # {category.name: category.confidence}, so that they can
        # be treated as a sparse vector.
        result[category.name] = category.confidence

    if verbose:
        print(text)
        for category in categories:
            print(u'=' * 20)
            print(u'{:<16}: {}'.format('category', category.name))
            print(u'{:<16}: {}'.format('confidence', category.confidence))

    return result

if __name__ == '__main__':
    text = "How does this work? By looking at labeled data our software can learn new objects and patterns. Of course, it only identifies objects it has learned about."
    print(classify(text))
