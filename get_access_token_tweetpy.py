import tweepy
import json

tweet_config = json.load(open('./tweet.json', 'r'))
CONSUMER_KEY = tweet_config['consumer_key']
CONSUMER_SECRET = tweet_config['consumer_secret']

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.secure = True
auth_url = auth.get_authorization_url()

print(f'Please authorize: {auth_url}')

verifier = input('PIN: ').strip()

auth.get_access_token(verifier)

print(f'ACCESS_TOKEN = {auth.access_token}')
print(f'ACCESS_TOKEN_SECRET = {auth.access_token_secret}')
