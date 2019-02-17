from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from twilio.rest import Client

app = Flask(__name__)
CORS(app)

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