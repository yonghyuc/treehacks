import pandas as pd
import os
from sklearn.utils import shuffle
import geolocation


class CrimeData:
    def __init__(self,
                 path,
                 split_ratio=0.7,
                 saved_data = True):
        self.path = path
        self.train_x = None
        self.train_y = None
        self.test_x = None
        self.test_y = None
        self.data = None
        self.split_ratio = split_ratio
        self.saved_data = saved_data


    def process_us_community_data(self):
        # grab community data from united states community
        community_data = pd.read_csv("./data/communities-crime-clean.csv")
        community_data['communityname'] = community_data['communityname'].str[:-4]

        places = list(community_data['communityname'])
        lat, lng, addr = [], [], []
        for ind, place in enumerate(places):
            ret_val = geolocation.getCoordinates(place)
            if len(ret_val) == 3:
                (lat_, lng_, addr_) = ret_val
                lat.append(lat_)
                lng.append(lng_)
                addr.append(addr_)
            else:
                community_data = community_data.drop(community_data.index[community_data.communityname == place])

            if ind % 100 == 0:
                print('Looking up %dth location' %ind)

        community_data = community_data.drop(columns=['communityname'])
        community_data['lat'] = lat
        community_data['lng'] = lng

        if not os.path.exists(self.path):
            os.mkdir(self.path)
        community_data.to_csv(self.path + '/us_community.csv', sep=',')

        self.data = community_data

    def split_data(self):
        if self.saved_data:
            self.data = pd.read_csv('./us_community.csv')
        self.data = shuffle(self.data)
        num_data = int(len(self.data)* self.split_ratio)
        self.train_x = self.data.iloc[:num_data, :]
        self.train_x = self.train_x[['lat', 'lng']].to_numpy()
        self.train_y = self.data.iloc[:num_data, :]
        self.train_y = self.train_y[['ViolentCrimesPerPop']].to_numpy()
        self.test_x = self.data.loc[num_data:, :]
        self.test_x = self.test_x[['lat', 'lng']].to_numpy()
        self.test_y = self.data.loc[num_data:, :]
        self.test_y = self.test_y[['ViolentCrimesPerPop']].to_numpy()



