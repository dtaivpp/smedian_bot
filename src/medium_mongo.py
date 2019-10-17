from pymongo import MongoClient
from mongo_generators import _get_all_generator, _update_one_generator

class Medium(object):
  def __init__(self):
    self.client = MongoClient()
    self.db = client["Medium"]
    self.Posts = db["Posts"]
    self.Collections = db["Collections"]
    self.Users = db["Users"]
    self.Publications = db["Publications"]

    # Generate the getter for all the documents in file
    self.get_all_Publications = _get_all_generator(self.Publications)
    self.get_all_Posts = _get_all_generator(self.Publications)
    self.get_all_Users = _get_all_generator(self.Publications)
    self.get_all_Collections = _get_all_generator(self.Publications)

    # Generate the update_one for single document in the database
    self.update_one_Publication = _update_one_generator(self.Publications)
    self.update_one_Post = _update_one_generator(self.Publications)
    self.update_one_User = _update_one_generator(self.Publications)
    self.update_one_Collection = _update_one_generator(self.Publications)
