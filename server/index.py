from flask import Flask, jsonify, request
import csv
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello():
    # Reads data.csv and renders it
    with open('../data.csv', 'r') as f:
        reader = csv.reader(f)
        headings = next(reader)
        output = []
        for row in reader:
            item = {heading: value_str for heading, value_str in zip(headings, row)}
            output.append(item)
        return jsonify(output)
    return jsonify({})
    
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
