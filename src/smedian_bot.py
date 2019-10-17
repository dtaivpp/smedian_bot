import scrape_smedian
import medium_mongo
seed_url = 'https://www.smedian.com/api/i/pub/advertised?bpa=true&limit=10&from=%7B"name"%3A"4IR%20Solutions"%2C"_id"%3A"5d9e2295dc57aecb0023b172"%7D'

def run_smedian_bot():
  smedian_fixed_their_data = False
  mediumDB = medium_mongo.Medium

  while not smedian_fixed_their_data:
  
    # Scrape
    smedian_pubs = scrape_smedian.get_publication_list(seed_url)
    
    # Updates
    updates(mediumDB, smedian_pubs)

    # Get Bad Publication

    # Tweet

    # Wait

  # Last Gasp Tweet Thank Smedian

  return

def updates(mediumDB,pubs):
  mediumDB.get
  pass
