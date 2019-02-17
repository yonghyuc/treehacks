from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from twilio.rest import Client
import requests
import datetime
import threading
from dateutil.relativedelta import relativedelta

storage = {}
app = Flask(__name__)
CORS(app)
timer = None

GOOGLE_MAP_API_KEY = "AIzaSyD3BRUfTSDs3AameaOGQ6oejQOZ32svP-c"
GOOGLE_MAP_API_URL = "https://maps.googleapis.com/maps/api/geocode/json"
TWILIO_SID = 'AC93d50f665e1e52813b6dabb120b18d1c'
PHONE_AUTH_1 = '08f9ef50c96d92b79677915be9165c47'


@app.route('/')
def hello():
    return "Hello"

@app.route('/test')
def test():
    return jsonify(storage)


@app.route('/phone_number/<number>')
def save_phone_number(number):
    storage["phone_number"] = number

    return jsonify({'success':True}), 200, {'ContentType':'application/json'}


@app.route('/test/sms')
def test_sms():
    account_sid = 'AC93d50f665e1e52813b6dabb120b18d1c'
    auth_token = '08f9ef50c96d92b79677915be9165c47'
    client = Client(account_sid, auth_token)

    client.messages.create(
        body="Hello world?!",
        from_='+13233065652',
        to='+13234960810'
    )

    return jsonify({'success':True}), 200, {'ContentType':'application/json'}

@app.route('/send_okay_sms')
def send_okay_sms():
    address = request.args.get('address', '?')
    account_sid = 'AC93d50f665e1e52813b6dabb120b18d1c'
    auth_token = '08f9ef50c96d92b79677915be9165c47'
    client = Client(account_sid, auth_token)
    # TODO: Angular app should handle the address and the location
    client.messages.create(
        body="I am okay. I am at " + address + " http://35.235.68.155:4200/receive",
        from_='+13233065652',
        to='+12137099805'
    )
    return "success"

@app.route('/send_help_sms')
def send_help_sms():
    address = request.args.get('address', '?')
    account_sid = 'AC93d50f665e1e52813b6dabb120b18d1c'
    auth_token = '08f9ef50c96d92b79677915be9165c47'
    client = Client(account_sid, auth_token)
    # TODO: Angular app should handle the address and the location
    client.messages.create(
        body="Help me! I am at " + address + " http://35.235.68.155:4200/receive",
        from_='+13233065652',
        to='+12137099805'
    )
    return "success"

@app.route('/status')
def send_check_status():
    client = Client(TWILIO_SID, PHONE_AUTH_1)

    client.messages.create(
        body="Are you ok?\nCould you tell us about your status?\nhttp://35.235.68.155:4200/status",
        from_='+13233065652',
        to='+13234960810'
    )
    return jsonify({'success':True}), 200, {'ContentType':'application/json'}

@app.route('/status/<status>')
def save_status(status):
    global timer

    storage["status"] = status
    storage["status_time"] = datetime.datetime.now()

    if (storage["status_time"] is True):
        timer.cancel()

    return jsonify({'success':True}), 200, {'ContentType':'application/json'}

@app.route('/receive')
def send_receiver_msg():
    client = Client(TWILIO_SID, PHONE_AUTH_1)

    client.messages.create(
        body="We are worrying about \"Mike\"\'s safety.\n Could you check on him?\nhttp://35.235.68.155:4200/receive",
        from_='+13233065652',
        to='+13234960810'
    )

    return jsonify({'success':True}), 200, {'ContentType':'application/json'}


@app.route("/security_score")
def data():
    global storage

    lat = request.args.get('lat')
    lng = request.args.get('lng')

    params = {
        'latlng': lat+","+lng,
        'key': GOOGLE_MAP_API_KEY
    }
    response = requests.get(GOOGLE_MAP_API_URL, params=params)
    jsonResult = response.json()
    result = jsonResult['results'][0]

    geodata = dict()
    geodata['lat'] = result['geometry']['location']['lat']
    geodata['lng'] = result['geometry']['location']['lng']
    geodata['address'] = result['formatted_address']

    storage['location'] = geodata
    storage['location_time'] = datetime.datetime.now()

    print(geodata)

    # CALL ML module
    # likelihood = ML_module.call(geodata)
    likelihood = 0.77

    if (likelihood > 0.6):
        send_check_status()
        send_receiver_msg()

    return jsonify({'score': 0.54, 'address': geodata['address']}), 200, {'ContentType':'application/json'}

def periodic():
    global timer
    diff = relativedelta(storage["status_time"], datetime.datetime.now())
    if (diff.minutes > 1):
        send_receiver_msg()

    if (storage["status"] is False):
        timer = threading.Timer(10, periodic)
        timer.start()

@app.errorhandler(500)
def server_error(e):
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500

if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END app]