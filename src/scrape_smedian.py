import requests
from random import randint
from time import sleep
import json
from copy import deepcopy
from random import randint

# Request data
def _request_data(url, retry=0):
  response = requests.get(url)
  data = {}

  if retry > 2:
    with open('error.log', 'w') as f:
      f.write("URL: {}\n Failed after 3 attemtps".format(url))

    raise Exception('Too many failed attempts')

  status = response.status_code

  if status == 200 or status == 202:
    data = response.json()  

  elif status == 404:
    _request_data(url, 3)

  else:
    sleep(randint(10, 20))
    _request_data(url, retry + 1)

  return data


# Extract page data
def _extract_data(data):
  last_pub_name, last_pub_id = None, None

  url_list = [item['url'] for item in data["values"]]

  if 'from' in data["paging"]:
    last_pub_name = data["paging"]["from"]["name"]
    last_pub_id = data["paging"]["from"]["_id"]

  return last_pub_name, last_pub_id, url_list


# Generate next url
def _generate_next_url(PubName, PubId):

  if PubName == None or PubId == None:
    raise AttributeError("PubName and PubId must have values. \
      PubName: {}, PubId: {}".format(PubName, PubId))

  baseurl = 'https://www.smedian.com/api/i/pub/advertised' + \
			'?bpa=true&limit=100&from=%7B%22name%22%3A%22'
  
  FormattedName = str(PubName).replace(" ", "%20")
  
  FormattedURL = "".join([baseurl, 
						  FormattedName, 
						  "%22%2C%22_id%22%3A%22", 
						  PubId, 
						  "%22%7D"])
  
  return FormattedURL


def get_publication_list(seed_url):
  """ 
  Returns all smedian publications in a list

  Input: Seed Url
  """
  
  url = deepcopy(seed_url)
  pub_list = []

  while url != None:
    data  = _request_data(url)
    nextPubName, nextPubId, urlList = _extract_data(data)
    
    pub_list = pub_list + urlList

    if nextPubName != None:
      url = _generate_next_url(nextPubName, nextPubId)
    
    else: url = None

    sleep(randint(2,6))

  return pub_list
