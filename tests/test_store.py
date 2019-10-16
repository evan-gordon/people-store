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

FOUR_VALID_PEOPLE = [
    Person({"age": 2}),
    Person({"age": 3}),
    Person({"age": 4}),
    Person({"age": 5})
]

def test_valid_phone_numbers_return_match():
  for x in VALID_PHONE_NUMBERS:
    person = Person({'number': x})
    assert not store.validate_person_phone_number(person) is None

def test_invalid_phone_numbers_return_none():
  for x in INVALID_PHONE_NUMBERS:
    person = Person({'number': x})
    assert store.validate_person_phone_number(person) is None

def test_store_all_if_list_isnt_full():
  youngest = [(1, Person({"age": 1}))]
  store.filter_old_people(youngest, FOUR_VALID_PEOPLE, 5)
  assert len(youngest) == 5

def test_filters_oldest_if_full():
  youngest = [(1, Person({"age": 1})), (1, Person({"age": 1}))]
  store.filter_old_people(youngest, FOUR_VALID_PEOPLE, 5)
  assert len(youngest) == 5
  assert youngest[-1][0] == 4

def test_handles_duplicate_ages_well():
  youngest = [
      (2, Person({"age": 2})), (3, Person({"age": 3})),
      (4, Person({"age": 4})), (5, Person({"age": 5})),
      (6, Person({"age": 6}))
  ]
  people = [Person({"age": 1})] * 5
  store.filter_old_people(youngest, people, 5)
  assert len(youngest) == 5
  assert youngest[-1][0] == 1
