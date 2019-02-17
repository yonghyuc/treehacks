# Imports the Google Cloud client library
from google.cloud import language
from google.cloud.language import enums, types
from datetime import date, timedelta
import requests
import numpy as np
import os
import six
import json
import csv
import crime_hist

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "My Project 3714-fb0cdf1c014f.json"


def get_news(keyword):
    params = "q={query}&language=en&from={time}&apiKey={key}".format(
        query=keyword,
        time=(date.today() - timedelta(1)).strftime('%Y-%m-%d'),
        key="d88270e1fe034130a92a3705a48752cd"
    )
    url = "{base}{params}".format(base='https://newsapi.org/v2/everything?', params=params)
    response = requests.get(url).json()['articles']
    return response


def analyze_entities(city,
                     threshold=-0.3):
    corpus = crime_hist.get_crime_words()
    response = get_news(city)
    temp =[]
    in_corpus, sentiment = [], []
    for res in response:
        text = res['description']
        client = language.LanguageServiceClient()
        incorpus = False

        if isinstance(text, six.binary_type):
            text = text.decode('utf-8')

        # Instantiates a plain text document.
        document = types.Document(
            content=text,
            type=enums.Document.Type.PLAIN_TEXT)

        # Detects entities in the document. You can also analyze HTML with:
        #   document.type == enums.Document.Type.HTML
        entities = client.analyze_entities(document).entities

        for entity in entities:
            counter = 0
            entity_type = enums.Entity.Type(entity.type)
            if entity_type.name == "EVENT":
                event = str(entity)
                event = event.split('\"')
                event = event[-2].lower()
                if event in corpus and get_sentiment(text)[0] < threshold:
                    in_corpus.append(1)
                    sentiment.append(get_sentiment(text))
                    incorpus = True
                    temp = res
                    break
        if not incorpus:
            in_corpus.append(0)
            sentiment.append(get_sentiment(text)[0])
    return [in_corpus, sentiment], temp



def news_sentiment(keyword):
    response = get_news(keyword)
    sen, mag = [], []
    for idx, res in enumerate(response):
        if idx > 100:
            break
        temp = get_sentiment(res['description'])
        sen.append(temp[0])
        mag.append(temp[1])
    return [np.mean(sen), np.mean(mag)]


def get_sentiment(str):
    # Instantiates a client
    client = language.LanguageServiceClient()

    # The text to analyze
    document = types.Document(
        content=str,
        type=enums.Document.Type.PLAIN_TEXT)

    # Detects the sentiment of the text
    sentiment = client.analyze_sentiment(document=document).document_sentiment
    return [sentiment.score, sentiment.magnitude]


def reverse_geocode_to_county(lat, lng):
    params = "latlng={lat},{lon}&sensor={sen}&key={key}".format(
        lat=lat,
        lon=lng,
        sen=True,
        key="AIzaSyCXtrBJP1qJyCXk_Ng--p6vCHxhUyXVi90"
    )
    url = "{base}{params}".format(base='https://maps.googleapis.com/maps/api/geocode/json?', params=params)
    response = requests.get(url).json()['results'][0]['address_components']
    for res in response:
        if res['types'] == ['administrative_area_level_2', 'political']:
            return res['long_name']


def reverse_geocode_to_town(lat, lng):
    params = "latlng={lat},{lon}&sensor={sen}&key={key}".format(
        lat=lat,
        lon=lng,
        sen=True,
        key="AIzaSyCXtrBJP1qJyCXk_Ng--p6vCHxhUyXVi90"
    )
    url = "{base}{params}".format(base='https://maps.googleapis.com/maps/api/geocode/json?', params=params)
    response = requests.get(url).json()['results'][0]['address_components']
    locality, state = ""
    for res in response:
        if res['types'] == ['locality', 'political']:
            locality = res['long_name']
        if res['types'] == ['administrative_area_level_1', 'political']:
            state = res['short_name']
    return [locality, state]


def main():
    cities = ['Davis', 'Houston']
    for city in cities:
        temp = analyze_entities(get_news(city), city)

    # news_data = []
    # for t in temp:
    #     news_data.append([t['title'], t['description']])

    # print(json.dumps(temp, indent=4, sort_keys=True))

    # print(get_news('Santa Clara County'))
    # print(get_news('San Mateo County'))


if __name__ == "__main__":
    main()

