# treehacks
TreeHacks 2019

## How to run the python backend server

```
$ cd server
$ pip install -r requirements.txt
$ FLASK_ENV=development FLASK_APP=main.py flask run
```

WINDOW
```
$ cd server
$ pip install -r requirements.txt
$ SET FLASK_ENV=development
$ SET FLASK_APP=index.py
$ pipenv run flask run
```

## How to run the angular frontend server
```
$ cd frontend
$ ng serve --open
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
