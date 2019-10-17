from pymongo import MongoClient

class Medium(object):
  def __init__(self):
    self.client = MongoClient()
    self.db = client["Medium"]
    self.Posts = db["Posts"]
    self.Collections = db["Collections"]
    self.Users = db["Users"]
    self.Publications = db["Publications"]


  #### Factories ####
  def _obj_dif_getter(self, oldObj, newObj):
    updatedObj = {}

    for key in newObj.keys():
      if key not in oldObj:
        continue

      if oldObj[key] == newObj[key]:
        continue
          
      updatedObj[key] = newObj[key]
    
    return updatedObj


  def get_all(self, collection):
    return collection.find({})


  def update_obj(self, collection, obj):
    """
    This method takes in an obj with an id and will update
      the object with the new data
    """
    if collection.count_documents({"_id": obj['_id']}) == 0:
      collection.insert_one(obj)
    else:
      old = collection.find_one({'_id': obj['_id']})

      updatedObj = self._obj_dif_getter(old, obj) 
      collection.update_one({'_id': obj['_id']}, {'$set': updatedObj}) 


  def delete_one(self, collection, obj):
    return collection.delete_one(obj['_id'])     


  def exists(self, collection, obj):
    return collection.count_documents({"_id": obj['_id']}) > 0



  #### Publication funcitons ####
  def delete_one_Publication(self, obj):
    return self.delete_one(self.Publications, obj)
    
  def exists_Publication(self, obj):
    return self.exists(self.Publications, obj)
    
  def get_all_Publications(self):
    return self.get_all(self.Publications)
     
  def update_one_Publication(self, obj):
    return self.update_obj(self.Publications, obj) 

