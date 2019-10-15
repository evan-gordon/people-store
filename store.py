# Business logic for person model
#
from requests import codes, get
from typing import Union
from people.person import Person
import bisect, json, re as regex

NUMBER_REGEX = regex.compile(
    "^(?:[0-9]{3}(?:-| )?|\([0-9]{3}\)(?:-| )?)?[0-9]{3}(?:-| )?[0-9]{4}$"
)

LIST_ENDPOINT = 'https://appsheettest1.azurewebsites.net/sample/list'
GET_PERSON_ENDPOINT = 'https://appsheettest1.azurewebsites.net/sample/detail/{}'

def get_youngest_people(max_number: int) -> Union[list, dict]:
  """
  Batch retreiving a group of people.
  For each batch retreive each person.
  Store the youngest `max_number` with valid phone numbers.

  Returns a list of people dictionaries or error dictionary
  """
  youngest_people = []
  curr_token = None
  while True:
    response = get_people_batch(curr_token)
    if (codes.ok != response.status_code):
      return error_response(LIST_ENDPOINT, curr_token, response)
    curr_token = response.json().get('token', None)
    ids_list = response.json().get('result', [])
    for id in ids_list:
      person_endpoint = GET_PERSON_ENDPOINT.format(id)
      person_response = get(person_endpoint)

      if (
          codes.ok == person_response.status_code and
          validate_phone_number(person_response.json().get('number', ""))
      ):
        person = Person(person_response.json())
        bisect.insort(youngest_people, (person.age, person))
        if (max_number < len(youngest_people)):
          youngest_people.pop()
    if (not curr_token):
      break
  result = []
  for (age, person) in youngest_people:
    result.append(person.__dict__)
  return result

def get_people_batch(token: str = None):
  if (token):
    return get(LIST_ENDPOINT, {'token': token})
  else:
    return get(LIST_ENDPOINT)

def error_response(endpoint: str, token: str, response: any) -> dict:
  """
  Generate an error response for returning to the FE.
  """
  params = ''
  if (token):
    params = f"?token={token}"
  return {
      'status_code': response.status_code,
      'type': 'GET',
      'endpoint': endpoint + params
  }

def validate_phone_number(number: str):
  """
  Matches the given phone number against the given Regex.

  Typically I avoid using Regexs' but in this scenario I can't know all
  Of the allowed formats for example `XXX.XXXX` thus for this project
  tailoring a regex to the currently avaliable test data seemed expedient.
  """
  number = number.strip()
  return NUMBER_REGEX.match(number)