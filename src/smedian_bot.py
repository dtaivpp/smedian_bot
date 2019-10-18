import scrape_smedian
import medium_mongo
from time import sleep
from random import randint
import twitter 
from os import environ

seed_url = 'https://www.smedian.com/api/i/pub/advertised?bpa=true&limit=10&from=%7B"name"%3A"4IR%20Solutions"%2C"_id"%3A"5d9e2295dc57aecb0023b172"%7D'

hashtags = [
  "#UmHello",
  "#AreYouThere",
  "#WhatsUp",
  "#WhyAreYouIgnoringMe",
  "#PlsRespond",
  "#CleanIt",
  "#TryingToHelp", 
  "#LetMeHelpYou",
  "#FakeNews",
  "#FixYourData",
  "#DoesAnyOneLogIn",
  "#ListenToMe",
  "#DoYouEvenCare",
  "#WhyLie",
  "#JustNotRight",
  "#DataCleanUp",
  "#TiredOfTweetingYou",
  "#JustLetMeSleep"
  "#RunningOutOfHashtags",
  "#RIP",
  "#CleanYourList", 
  "#MoshiMosh",
  "#IsAnyoneHome"
]

tweetTemplate = [
  "@smedian_network You all have this url listed as a publication but it doesnt exist? ¯\_(ツ)_/¯ \n #Smedian {} \n {}",
  "@smedian_network Hey I think you all may want to remove this publication. Its ded \n #Smedian {} \n {}",
  "@smedian_network Not sure if this is intentional but this publication is dead.... \n #Smedian {} \n {}",
  "@smedian_network You all seem to have some data issues. This publication doesnt exist... \n #Smedian {} \n {}",
  "@smedian_network Let me help you. Here is another publication that doesnt exits \n #Smedian {} \n {}",
  "@smedian_network I literally have a whole list of publications of yours that dont work. \n #Smedian {} \n {}",
  "@smedian_network I could send you the list of bad publicaions but youuu wont talk to me. \n #Smedian {} \n {}",
  "@smedian_network oh.... look at that... another bad publication...  \n #Smedian {} \n {}",
  "@smedian_network RIP your inbox. Just clean your publicaiton list and I can stop tweeting these at you. \n #Smedian {} \n {}",
  "@smedian_network Help. Me. Help. You. Remove the ded links. Here is another fyi. \n #Smedian {} \n {}",
  "@smedian_network Fyi I dont really find this fun... here's another ded publication.  \n #Smedian {} \n {}",
  "@smedian_network Row row row your boat through the dead publications...  \n #Smedian {} \n {}",
  "@smedian_network Instead of me coming up with clever tweets how about you clean your publication list? ¯\_(ツ)_/¯ \n #Smedian {} \n {}",
  "@smedian_network Please... clean your list. another bad pub \n #Smedian {} \n {}",
  "@smedian_network If you clean your bad publications I wont have anything to tweet about ¯\_(ツ)_/¯ \n #Smedian {} \n {}",
  "@smedian_network What if instead of ignoring me you clean your list ¯\_(ツ)_/¯ \n #Smedian {} \n {}",
  "@smedian_network Hey guys, just figured you would want to know this publicaiton is dead. \n #Smedian {} \n {}",
  "@smedian_network Here is another dead publication \n #Smedian {} \n {}",
  "@smedian_network I found this dead publication in your list. Could you remove it? \n #Smedian {} \n {}",
  "@smedian_network Moshi mosh! another dead publication for your list \n #Smedian {} \n {}",
  "@smedian_network I do contract work. Hire me and I can clean your publication list quicker. Oh and here is another \n #Smedian {} \n {}",
  "@smedian_network I'm the bad guy, duh #BillieEilish Jk just clean your publications and I wont have to be.  \n #Smedian {} \n {}",
  "@smedian_network 404 orginization that cares not found. Hey but on the good side I found a.... oh nope this link is dead too... \n #Smedian {} \n {}",
  "@smedian_network I think you may have a bad count of publicaions. Because this one doesnt exist anymore. \n #Smedian {} \n {}",
]

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
    smedian_fixed_their_data = sendTweet(pub['_id'])    

    # Wait
    sleep(randint(3600,7200))
    

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

def sendTweet(url, body=''):
  value = False
  twiAPI = twitter.Api(consumer_key=[environ.get('twitterKey')],
                      consumer_secret=[environ.get('twitterSecret')],
                      access_token_key=[environ.get('twitterAccessToken')],
                      access_token_secret=[environ.get('twitterAccessSecret')],
                      input_encoding='utf8')

  tag = hashtags[randint(0, len(hashtags) - 1)]
  
  if body == '':
    body = tweetTemplate[randint(0, len(tweetTemplate) - 1)].format(tag, url)

  try:
    mentions = twiAPI.GetMentions()
    dms = twiAPI.GetDirectMessages()

    for mention in mentions:
      if mention['sender_id'] == "@smedian_network":
        value = True
    
    for dm in ['sender_id'] == "@smedian_network":
        value = True

    if not value:
      twiAPI.PostUpdate(
        body
      )
  except:
    pass

  return value


if __name__ == '__main__':
  run_smedian_bot()