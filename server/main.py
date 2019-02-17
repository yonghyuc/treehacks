from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from twilio.rest import Client
import requests

app = Flask(__name__)
CORS(app)

GOOGLE_MAP_API_KEY = "AIzaSyD3BRUfTSDs3AameaOGQ6oejQOZ32svP-c"
GOOGLE_MAP_API_URL = "https://maps.googleapis.com/maps/api/geocode/json"
TWILIO_SID = 'AC93d50f665e1e52813b6dabb120b18d1c'
PHONE_AUTH_1 = '08f9ef50c96d92b79677915be9165c47'


@app.route('/')
def hello():
    return "Hello"

@app.route('/test')
def test():
    output = {'abc': 100}
    return jsonify(output)

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

    return "success"

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
    return "success"

@app.route('/receive')
def send_receiver_msg():
    client = Client(TWILIO_SID, PHONE_AUTH_1)

    client.messages.create(
        body="We are worrying about \"Mike\"\'s safety.\n Could you check on him?\nhttp://35.235.68.155:4200/receive",
        from_='+13233065652',
        to='+13234960810'
    )
    return "success"

@app.route("/security_score")
def data():
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

    print(geodata)

    # CALL ML module
    # likelihood = ML_module.call(geodata)
    likelihood = 0.77

    if (likelihood > 0.6):
        send_check_status()

    if (likelihood > 0.75):
        send_receiver_msg()

    result = {
        'score': likelihood
    }

    return jsonify(result), 200, {'ContentType':'application/json'}

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