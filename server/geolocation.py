import requests

def getCoordinates(place):
    KEY = "AIzaSyCXtrBJP1qJyCXk_Ng--p6vCHxhUyXVi90"
    GOOGLE_MAPS_API_URL = 'https://maps.googleapis.com/maps/api/geocode/json'

    params = {
        'address': place,
        'sensor': 'false',
        'region': 'us',
        'key': KEY
    }
    try:
        res = requests.get(GOOGLE_MAPS_API_URL, params=params).json()['results'][0]
        lat =(res['geometry']['location']['lat'])
        lng=(res['geometry']['location']['lng'])
        addr=(res['formatted_address'])
        return lat, lng, addr
    except:
        print('Error encountered for %s' % (place))
        return place




