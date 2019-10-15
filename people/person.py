class Person:

  def __init__(self, json):
    self.id = json.get('id', None)
    self.name = json.get('name', None)
    self.age = json.get('age', None)
    self.number = json.get('number', "")
    self.photo = json.get('photo', None)
    self.bio = json.get('bio', None)
