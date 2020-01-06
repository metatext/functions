from google.cloud import language

import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="./API-project-credentials.json"

def sentiment_text(text):

    client = language.LanguageServiceClient()

    sentiment = client.analyze_sentiment(text).document_sentiment

    print('Score: {}'.format(sentiment.score))
    print('Magnitude: {}'.format(sentiment.magnitude))

sampletxt='Python is great'

sentiment_text(sampletxt)
