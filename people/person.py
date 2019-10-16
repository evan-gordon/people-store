class Person:
  """
  Simple Person object for validation of person json.

  I could have used a django model here but I opted not to as
  my solution didn't really require a database. 
  """

  def __init__(self, json):
    self.id = json.get('id', None)
    self.name = json.get('name', "")
    self.age = json.get('age', 999)
    self.number = json.get('number', "").strip()
    self.photo = json.get('photo', "")
    self.bio = json.get('bio', "")
