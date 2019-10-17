from pymongo import MongoClient
from mongo_generators import _get_all_generator, \
                             _update_one_generator, \
                             _exists_generator, \
                             _delete_one_generator

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
    self.get_all_Posts = _get_all_generator(self.Posts)
    self.get_all_Users = _get_all_generator(self.Users)
    self.get_all_Collections = _get_all_generator(self.Collections)

    # Generate the update_one for single document in the database
    self.update_one_Publication = _update_one_generator(self.Publications)
    self.update_one_Post = _update_one_generator(self.Posts)
    self.update_one_User = _update_one_generator(self.Users)
    self.update_one_Collection = _update_one_generator(self.Collections)

    # Generate the check if exists funcitons
    self.exists_Publication = _exists_generator(self.Publications)
    self.exists_Post = _exists_generator(self.Posts)
    self.exists_User = _exists_generator(self.Users)
    self.exists_Collection = _exists_generator(self.Collections)

    # Generate delete functinon for objects
    self.delete_one_Publication = _delete_one_generator(self.Publications)
    self.delete_one_Post = _delete_one_generator(self.Posts)
    self.delete_one_User = _delete_one_generator(self.Users)
    self.delete_one_Collection = _delete_one_generator(self.Collections)