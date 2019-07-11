from twython import Twython
import json

tweet_config = json.load(open('./tweet.json', 'r'))
CONSUMER_KEY = tweet_config['consumer_key']
CONSUMER_SECRET = tweet_config['consumer_secret']
ACCESS_TOKEN = tweet_config['access_token']
ACCESS_TOKEN_SECRET = tweet_config['access_token_secret']


twitter = Twython(CONSUMER_KEY, CONSUMER_SECRET,
                  ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

def tweet(msg, img=None):
  if img is not None:
    photo = open(img, 'rb')
    response = twitter.upload_media(media=photo)
    twitter.update_status(status=msg, media_ids=[response['media_id']])
  else:
    twitter.update_status(status=msg)

def delete_tweets():
  while True:
    #get the timeline
    timeline = twitter.get_user_timeline(count=200)

    if len(timeline) == 0:
      print("No tweets left to delete")
      break

    #delete the timeline
    for tweet in timeline:
      while True:
        print(f'Tweet: {tweet["text"]}')
        user_input = input('Do you want to delete this tweet (Y/n):')
        if user_input == 'y' or user_input == '':
          status = int(tweet['id_str'])
          twitter.destroy_status(id=status)
          print(f'Tweet deleted: {status}')
          break
        elif user_input == 'n':
          print(f'Tweet not deleted: {status}')
          break
        else:
          print('Please write Y or n')
    print(f'{len(timeline)} tweets remaining')
