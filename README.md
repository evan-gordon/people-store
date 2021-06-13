# People Store

**One off demo project, not in active development**

Stores information about people from a given endpoint.

## Installation

You will need:

* python3.7.4 <https://www.python.org/downloads/>
* pip <https://pip.pypa.io/en/stable/installing/>
* pipenv <https://pypi.org/project/pipenv/>

And that's it!

## To Run

Navigate to the project root directory. Then run:

```bash
pipenv shell
pipenv install
python manage.py runserver
```

or to run tests:

```bash
pytest -q
```

Congratulations! You can now run your server from <localhost:8000>

## Regarding the Solution

These are my thoughts regarding the scenario where we encounter a dataset that is much larger than we currently have.<br/>

Ideally, we could move to a more proactive event sourcing architecture. We could use a tool such as Apache Kafka to listen to events and then setup the server containing people to push out updates to this service through a Kafka producer/consumer setup.
If we however cannot affect the architecture of how we retrieve people data server then the best we could do would be to run a periodic task to query for and cache the data it gets. This way we could at least mitigate the amount of network calls required to get the information we need.

## Commands Used During Setup

```bash
django-admin startproject peoplestore
cd peoplestore && pipenv shell
pipenv install django flake8 yapf requests pytest
python manage.py startapp people
```
