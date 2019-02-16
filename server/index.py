from flask import Flask, jsonify, request
import csv
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""

    def string_to_value(heading, value_str):
        # There might be a case that non-boolean starts with "is_" or "has_", but
        # for saving time, I woule like to do this.
        if heading.startswith('is_') or heading.startswith('has_') or heading == 'tournament':
            if value_str == 'True':
                return True
            elif value_str == 'False':
                return False
            else:
                raise Exception('Unexpected value. Not True, not False: ' + value_str)
        if heading == 'num_options' or heading == 'question_id':
            return int(value_str)
        return value_str

    with open('../questions.csv', 'r') as f:
        reader = csv.reader(f)
        headings = next(reader)
        output = []
        for row in reader:
            item = {heading: string_to_value(heading, value_str) for heading, value_str in zip(headings, row)}
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
