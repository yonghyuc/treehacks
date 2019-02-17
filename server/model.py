import numpy as np 
import pandas as pd 
import datetime
import urllib
import os
from sklearn.neighbors import KNeighborsRegressor
import pickle
import nlp_news

# module pulling and processing US general community crime data
from process_data import *
from geolocation import *
from nlp_news import *

knn = pickle.load(open("model_0.34307634520580066.sav", "rb"))

class KNN:
    def __init__(self,
                 data,
                 k=None):
        self.score_list = []
        self.data=data

        if not k:
            for k in range(1, min(10, len(data.train_x))):
                self.model = KNeighborsRegressor(n_neighbors=k)
                self.model.fit(data.train_x, data.train_y)
                self.score_list.append(self.model.score(self.data.test_x, self.data.test_y))
            k = np.argmax(np.array(self.score_list)) + 1
        self.model = KNeighborsRegressor(n_neighbors=k)
        self.model.fit(self.data.train_x, self.data.train_y)

    def predict(self,
                location):
        return self.model.predict(location)

    def score(self):
        return self.model.score(self.data.test_x, self.data.test_y)


def get_output(lat, lon):
    
    y_hat = knn.predict(np.array([lat, lon]).reshape(1,2))
    city = reverse_geocode_to_county(lat, lon)
    (sentiment, news) = analyze_entities(city)
    res = []
    if news:
        res.append(news['title'])
    bol = [sentiment[i][0] for i in range(len(sentiment))]
    sent = [sentiment[i][1] for i in range(len(sentiment))]
    bol = np.array(bol)
    sent = np.array(sent)
    perc = np.mean(bol) # percentage of true false

    if perc == 0:
        return y_hat, []
    avg_score_of_pos = np.mean(np.abs((sent[bol > 0])))
    numerator= 0.8*perc + 0.2*avg_score_of_pos
    final_danger_score = 0.6*numerator + 0.4*y_hat
    final_danger_score = float(final_danger_score)
    print(final_danger_score, res)
    return final_danger_score, res
