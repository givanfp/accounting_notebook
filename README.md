# Accounting notebook

## Building

It is best to use the python `virtualenv` tool to build locally:

```sh
$ virtualenv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
$ python manage.py migrate
$ python manage.py runserver
```

Then visit `http://localhost:8000` to view the app. 

Browsable API in `http://localhost:8000/api/transactions/`

To run unit tests:
```
$ python manage.py test myapp
```
