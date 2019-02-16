from flask import Flask, jsonify, request
import csv
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello():
    # Reads data.csv and renders it
    output = {'abc': 100}
    return jsonify(output)
    
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
