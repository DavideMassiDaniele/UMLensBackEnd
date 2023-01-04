# UMLens server

## Prerequisites

Before continue, assert you have **Python3** installed in your machine.

## Requirements

Create new `venv` and activate it:
```bash
$ python3 -m pip venv venv
$ source venv/bin/activate
```

Install `requirements.txt` with following command:
```bash
$ pip install -r requirements.txt
```

## Usage

To start the server locally you have to use:
```bash
$ python3 main.py
```

To start server in a production environment:
```bash
$ gunicorn main:app
```