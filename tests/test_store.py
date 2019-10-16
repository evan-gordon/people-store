import pytest
from people.person import Person
import store

VALID_PHONE_NUMBERS = [
    '(111) 111-1111', '(111)111-1111', '(111) 111 1111', '111-111-1111',
    '111 111-1111', '111-1111', '123-456-7890'
]

INVALID_PHONE_NUMBERS = [
    '', '111 111-111', '111-111', '111 111', '5555', '101', '111', '9'
]

def test_valid_phone_numbers_return_match():
  for x in VALID_PHONE_NUMBERS:
    person = Person({'number': x})
    print(x)
    assert not store.validate_person_phone_number(person) is None

def test_invalid_phone_numbers_return_none():
  for x in INVALID_PHONE_NUMBERS:
    person = Person({'number': x})
    assert store.validate_person_phone_number(person) is None