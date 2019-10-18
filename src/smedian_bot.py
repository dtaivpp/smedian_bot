import scrape_smedian
import medium_mongo
from time import sleep
from random import randint
seed_url = 'https://www.smedian.com/api/i/pub/advertised?bpa=true&limit=10&from=%7B"name"%3A"4IR%20Solutions"%2C"_id"%3A"5d9e2295dc57aecb0023b172"%7D'

def run_smedian_bot():
  smedian_fixed_their_data = False
  mediumDB = medium_mongo.Medium()

  while not smedian_fixed_their_data:
  
    # Scrape
    smedian_pubs = scrape_smedian.get_publication_list(seed_url)
    
    # Updates
    updates(mediumDB, smedian_pubs)

    # Get Bad Publication
    pub = mediumDB.get_bad_Publication()
    if pub == None:
      smedian_fixed_their_data = True
      continue

    # Tweet
    print("Id be tweeting here about {}".format(pub['_id']))    

    # Wait
    sleep(randint(3600,7200))

  # Last Gasp Tweet Thank Smedian
  print("Ayyy you all fixed it! GG")

  return

def create_pub(url):
  return {
    '_id': url,
    'url': url,
    'last_scraped':None,
    'active': True, 
    'smedian_publication': True,
    'tweeted': 0
  }
  

def deactivate_pub(url):
  return {
    '_id': url,
    'smedian_publication': False
  }


def compare_pubs(newPubs, oldPubs):
  """ Input: newPubs: list, oldPubs: dict """
  addPubs = {}
  
  for pub in newPubs:
    if pub in oldPubs:
      oldPubs.pop(pub)
    else: 
      addPubs[pub] = create_pub(pub)

  return oldPubs, addPubs


def updates(mediumDB, pubs):
  currPubList = mediumDB.get_all_Publications()
  
  deactivate, create = compare_pubs(pubs, currPubList)

  for item in deactivate.keys():
    mediumDB.upsert_one_Publication( deactivate_pub(item) )
  
  for item in create.keys():
    mediumDB.upsert_one_Publication(create[item])
  
  return 


if __name__ == '__main__':
  run_smedian_bot()