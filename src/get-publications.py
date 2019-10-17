import requests
from random import randint
from time import sleep
import json


def get_publications(url):
  PubName, PubId = "", ""
  NextFlag = True
  with open("urls.csv", "a") as f:
    while NextFlag:
      f.write("{}\n".format(url))

    data = request_data(url)
    try: 
      PubName, PubId = extract_data(data)
      url = generate_next_url(PubName, PubId)
    except: 
      NextFlag = False

    sleep(randint(4,10))

  return

def extract_data(data):
  with open("publications.csv", 'a', encoding="utf8") as f:
    for item in data["values"]:
      f.write("{}\n".format(item["url"]))
      print(item["url"])

  return data["paging"]["from"]["name"], data["paging"]["from"]["_id"]


def request_data(url):
  response = requests.get(url)
  return response.json()

def generate_next_url(PubName, PubId):
  baseurl = 'https://www.smedian.com/api/i/pub/advertised' + \
			'?bpa=true&limit=100&from=%7B%22name%22%3A%22'
  FormattedName = str(PubName).replace(" ", "%20")
  FormattedURL = "".join([baseurl, 
						  FormattedName, 
						  "%22%2C%22_id%22%3A%22", 
						  PubId, 
						  "%22%7D"])
  return FormattedURL

def useJSON(_json):
  extract_data(_json)
  return


if __name__=="__main__":
  with open("smedian.json", 'r', encoding="utf8") as f:
    data = f.read()
    extract_data(json.loads(data))
  #get_publications("https://www.smedian.com/api/i/pub/advertised?bpa=true&limit=820&from=%7B%22name%22%3A%22%3C%20BE%20OUTSTANDING%20%2F%3E%22%2C%22_id%22%3A%225927167d5fbc457423b176fc%22%7D")

  print("Fin")