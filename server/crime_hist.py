import json
import requests
from pandas.io.json import json_normalize
from nltk.corpus import wordnet
import nltk


def get_synm(word):
    synonyms = []

    for syn in wordnet.synsets(word):
        for l in syn.lemmas():
            synonyms.append(l.name())
    return synonyms


def get_crime_words():
    # from exploratory data analysis
    lim=8
    crime_words = ['shooting', 'attack', 'assault', 'killing', 'murder', 'police', 'panic','death']
    corpus = set()
    for word in crime_words:
        synm = corpus.get_synm(word)[:lim]
        for s in synm:
            corpus.add(s)
    return corpus


def criminal_hist(lat, lng, r=20):
    base = 'http://opendata.mybluemix.net/crimes?'
    params = "lat={lat}&lon={lng}&radius={r}".format(
        lat=lat,
        lng=lng,
        r=r
    )
    url = "{base}{params}".format(base=base, params=params)
    response = json.loads(requests.get(url).text)
    return json_normalize(response['results'])


