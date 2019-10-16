# Business logic for person model
#
from requests import adapters, exceptions, codes, Session
from typing import Tuple, Union
from people.person import Person
from web import url
import bisect, json, re as regex

NUMBER_REGEX = regex.compile(
    "^(?:[0-9]{3}(?:-| )?|\([0-9]{3}\)(?:-| )?)?[0-9]{3}(?:-| )?[0-9]{4}$"
)

LIST_ENDPOINT = 'https://appsheettest1.azurewebsites.net/sample/list'
GET_PERSON_ENDPOINT = 'https://appsheettest1.azurewebsites.net/sample/detail/{}'
TIMEOUT = 10

def get_youngest_people(max_number: int) -> Union[list, dict]:
  """
  Batch retreiving a group of people.
  For each batch retreive each person.
  Store the youngest `max_number` with valid phone numbers.

  Returns a list of people dictionaries or error dictionary
  """
  curr_token = None
  youngest_people = []
  with Session() as session:
    session.mount('https://', adapters.HTTPAdapter(max_retries=5))

    response = url.get(session, LIST_ENDPOINT)
    if (type(response) == dict): return response
    ids_list, curr_token = get_response_info(response)
    people = get_people_by_person_id(
        session, ids_list, keep=validate_person_phone_number
    )
    if (type(people) == dict): return people

    while curr_token:
      response = url.get(
          session, LIST_ENDPOINT, params={'token': curr_token}
      )
      if (type(response) == dict): return response
      ids_list, curr_token = get_response_info(response)
      people = get_people_by_person_id(
          session, ids_list, keep=validate_person_phone_number
      )
      print(people)
      if (type(people) == dict): return people
      # store in youngest list if not full or if curr person age
      # is less than max person age in list
      for person in people:
        if (
            len(youngest_people) == max_number and
            person.age < youngest_people[-1][0]
        ):
          bisect.insort(youngest_people, (person.age, person))
          youngest_people.pop()
        elif (len(youngest_people) < max_number):
          bisect.insort(youngest_people, (person.age, person))
  return [person.__dict__ for (age, person) in youngest_people]

# returns list of people
# can filter using the keep field
def get_people_by_person_id(
    session: any, ids_list: list, *, keep=lambda x: True
):
  """
  Using the given list call the get person endpoint
  if the call fails (timeout, retry failure or invalid return)
  returns a error dict
  otherwise returns a list of people

  result can be filtered by passed lambda `keep`
  lambda must accept a person object
  """
  result = []
  for id in ids_list:
    person_response = url.get(session, GET_PERSON_ENDPOINT.format(id))
    if (
        type(person_response) == dict and
        person_response.get('status_code') != 500 and
        person_response.get('status_code') != 404
    ):
      return person_response
    elif (
        type(person_response) != dict and
        codes.ok == person_response.status_code
    ):
      person = Person(person_response.json())
      if (keep(person)):
        result.append(person)
  return result

def validate_person_phone_number(person):
  """
  Matches the given person's phone number against the given Regex.

  Typically I avoid using Regexs' but in this scenario I can't know all
  Of the allowed formats for example `XXX.XXXX` thus for this project
  tailoring a regex to the currently avaliable test data seemed expedient.
  """
  number = person.number
  return NUMBER_REGEX.match(number)

def get_response_info(response: any) -> Tuple:
  json = response.json()
  return json.get('result', []), json.get('token', None)