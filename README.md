# People Store

Stores information about people from a given endpoint.

## Insallation

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

Congratulations! You can now run your server from <localhost:8000>

## Regarding the Solution

In the scenario where we encounter a dataset that is much larger than we currently have.
I could store all of the people data into my own database but depending on the arcitecture we could just end up duplicating data, however we would have the advantage of being able to directly query the database.
Here we would still need to perform some cache validation periodically or with every call to our endpoint in order maintain consistency.

A simpler solution would be to shard out the work for processing data. Depending on the arcitecture we could store page tokens. We then assign each process a in essence a starting and ending location for processing via the tokens.

Of course at some arbirarily large dataset size our call will eventually time out and we may need to switch to using a websocket for example in order to not cause a timeout in the browser or the aforementioned database solution.

## Commands Used During Setup

```bash
django-admin startproject peoplestore
cd peoplestore && pipenv shell
pipenv install django flake8 yapf requests
python manage.py startapp people
```
