from pymongo import MongoClient
import math

def get_twitter_currCount(publications):
    tweets = publications.aggregate([
      {
        '$match': {
          'smedain_publication': True, 
          'active': False,
        }
      },
      {
        '$group': {
          '_id': '',
          'tweeted': {'$sum': '$tweeted'}
        }
      },
      {
        '$project':{
          '_id': 0,
          'tweetedAmnt': '$tweeted'
        }
      }
    ])
    tweetNum = 0
    
    for item in tweets:
      tweetNum = tweetNum + item['tweetedAmnt']

    invalid = publications.count({'smedain_publication': True, 'active': False,})
    if invalid != 0 and tweetNum != 0:
      tweetNum = math.floor(tweetNum / invalid)
    
    return tweetNum

class Medium(object):
  def __init__(self):
    self.client = MongoClient('192.168.1.182',27017)
    self.db = self.client["Medium"]
    self.Posts = self.db["Posts"]
    self.Collections = self.db["Collections"]
    self.Users = self.db["Users"]
    self.Publications = self.db["Publications"]
    self.TwitterCurrCount = get_twitter_currCount(self.Publications)    


  #### Factories ####
  def _obj_dif_getter(self, oldObj, newObj):
    updatedObj = {}

    for key in newObj.keys():
      if key not in oldObj:
        updatedObj[key] = newObj[key]
        continue

      if oldObj[key] == newObj[key]:
        continue
          
      updatedObj[key] = newObj[key]
    
    return updatedObj


  def get_all(self, collection):
    _retDict = {}
    for item in collection.find({}):
      _retDict[item['_id']] = item

    return _retDict


  def upsert_obj(self, collection, obj):
    """
    This method takes in an obj with an id and will update
      the object with the new data
    """
    if collection.count({"_id": obj['_id']}) == 0:
      collection.insert_one(obj)
    else:
      old = collection.find_one({'_id': obj['_id']})

      updatedObj = self._obj_dif_getter(old, obj) 
      if len(updatedObj.keys()) != 0:
        collection.update_one({'_id': obj['_id']}, {'$set': updatedObj}) 
  
    return

  def tweeted_increment(self, obj):
    tweeted = self.Publication.find_one({'_id': obj['id']})
    updated_tweeted = 1

    if 'tweeted' in tweeted:
      updated_tweeted = tweeted['tweeted'] + 1
    
    self.Publications.update_one({
      '_id': obj['_id'], 
      '$set':{
        'tweeted': updated_tweeted
      }
    })
    
    return



  def delete_one(self, collection, obj):
    return collection.delete_one(obj['_id'])     


  def exists(self, collection, obj):
    return collection.count({"_id": obj['_id']}) > 0



  #### Publication funcitons ####
  def delete_one_Publication(self, obj):
    return self.delete_one(self.Publications, obj)
    
  def exists_Publication(self, obj):
    return self.exists(self.Publications, obj)
    
  def get_all_Publications(self):
    return self.get_all(self.Publications)

  def upsert_one_Publication(self, obj):
    if len(obj.keys()) == 0:
      return 
    
    return self.upsert_obj(self.Publications, obj) 

  def get_bad_Publication(self):
    count = 0

    pub = self.Publications.find_one(
      {
        'smedian_publication': True, 
        'active': False,
        '$or':[
            {'tweeted': {'$exists': False}},
            {'tweeted': {'$lt': self.TwitterCurrCount}}
          ]
      }
    )

    # If there are no publications see if there are 
    #   still invlaid publications belonging to smedain
    if pub != None:
      return pub
    
    count = self.Publications.count(
      {
      'smedian_publication': True, 
      'active': False
      }
    )

    # If none return none
    if count == 0:
      return None
    
    # Otherwise increment the twitter count number and
    #   repeat the operation 
    self.TwitterCurrCount = self.TwitterCurrCount + 1
    self.get_bad_Publication()

