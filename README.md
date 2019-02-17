# treehacks
TreeHacks 2019

## How to run the web server

```
$ cd server
$ pip install -r requirements.txt
$ FLASK_ENV=development FLASK_APP=index.py pipenv run flask run
```

then open http://localhost:5000/


## How to deploy

Install Google Cloud SDK https://cloud.google.com/sdk/docs/

```
$ cd server
$ gcloud app deploy --project=treehacks-mappal
```

then

```
$ gcloud app browse --project=treehacks-mappal
```

or open https://treehacks-mappal.appspot.com/

We can get a fancy domain later.