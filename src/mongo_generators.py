def _obj_dif_getter(oldObj, newObj):
  updatedObj = {}

  for key in newObj.keys():
    if key not in oldObj:
      continue

    if oldObj[key] == newObj[key]:
      continue
        
    updatedObj[key] = newObj[key]
  
  return updatedObj


def _get_all_generator(collection):
  """
  This returns a get function that gets all 
    the documents from a collection
  """

  def get_all():
    return collection.find({})

  return get_all


def _update_one_generator(collection):
  """ 
  Here we are creating mentods for updating one object in the database
  """
  def update_obj(obj):
    """
    This method takes in an obj with an id and will update
      the object with the new data
    """
    if collection.count_documents({"_id": obj['_id']}) == 0:
      collection.insert_one(obj)
    else:
      old = collection.find_one({'_id': obj['_id']})

      updatedObj = _obj_dif_getter(old, obj) 
      collection.update_one({'_id': obj['_id']}, {'$set': update_obj}) 


def _exists_generator(collection):

  def exists(obj):
    return collection.count_documents({"_id": obj['_id']}) > 0
  
  return exists