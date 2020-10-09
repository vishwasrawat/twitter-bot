import tweepy #tweepy (library to access twitter API)
import time
import requests
from bs4 import BeautifulSoup

#auth twitter
consumer_key = r"XXXXXXXXXXXXXXXXXXXXXXXXXXXX"
consumer_secret = r"XXXXXXXXXXXXXXXXXXXXXXXXXXXX"
access_token = r"XXXXXXXXXXXXXXXXXXXXXXXXXXXX"
access_token_secret = r"XXXXXXXXXXXXXXXXXXXXXXXXXXXX" 

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)


#first step would be - running all the functions; 
#input - id file in text - Note intially the file will contain the tweet id of the tweet from, where you want to update the status

id_file_path = r"ids.text"

def retrive_last_id(ids_file):
  with open(ids_file, "r") as f:
    last_id = f.read()
  return last_id

def store_last_id(ids_file, id):
  with open(ids_file, "w+") as f:
    last_id = f.write(str(id))

def match_status():
  live_score_url = r"https://www.cricbuzz.com/cricket-series/3130/indian-premier-league-2020"
  req = requests.get(live_score_url)
  soup = BeautifulSoup(req.content, 'html.parser')
  
  team = soup.find_all("div", class_="matchscag-name")
  first_team = team[0].get_text()
  second_team = team[1].get_text()

  team_score = soup.find_all("div", class_="pull-right matchscag-scr-width")
  first_team_score = team_score[0].get_text()
  second_team_score = team_score[1].get_text()

  return first_team, second_team, first_team_score, second_team_score

def match_comment():
  ipl_url = r"https://www.cricbuzz.com/cricket-series/3130/indian-premier-league-2020/matches"
  req = requests.get(ipl_url)
  soup = BeautifulSoup(req.content, 'html.parser')
  sample_list = soup.find_all("a",class_="cb-text-complete")

  return sample_list[-1].get_text()


def reply_tweet(last_id):

  #a speical case when there is no score 
  print("reply to tweet")

  mentions = api.mentions_timeline(since_id = int(last_id))
  if len(mentions) is not 0:
    print("tweet")
    first_team, second_team, first_team_score, second_team_score = match_status()
    comment = match_comment()

    text = "IPL update\n"
    text = text + str(first_team) + ": " + str(first_team_score) + " & " + str(second_team) + ": " 
    text = text + str(second_team_score) + "\n" + str(comment)

    mentions.reverse()
    
    for mention in mentions:
      username = mention.user.screen_name
      id = mention.id
      api.update_status("@" + str(username) + "\n" + str(text), id)
      l_id = mentions[-1].id

  #media_url = points_table()
  
  else:
    print("no_tweet")
    l_id = last_id
  
  return l_id


while True:
  last_id = retrive_last_id(id_file_path) #will give us the last id of which we have replied. 
  new_last_id = reply_tweet(last_id)
  store_last_id(id_file_path, new_last_id) #return nothing - doubt will update the id status?
  time.sleep(15)
