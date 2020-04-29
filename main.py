import json
import random
import threading
from twython.exceptions import TwythonError
from tweet import tweet
from tweet import init as init_tweet
from generate_image import draw_participants
from enum import Enum
from time import sleep
import datetime as dt
import os

config = json.load(open('./config.json', 'r'))

def add_dead_participant(participant):
    if os.path.exists('dead.txt'):
        with open('dead.txt', 'a') as f:
            f.write(participant.name + '\n')
    else:
        with open('dead.txt', 'w') as f:
            pass

class Participant:
    def __init__(self, name):
        self.name = name
        self.alive = True

    def isalive(self):
        return self.alive

    def kill(self):
        self.alive = False
        add_dead_participant(self)

def get_participants():
    participants = []
    with open('participants.txt', 'r') as f:
        while True:
            line = f.readline()
            if line == '':
                break
            name = line.replace('\n', '')
            participants.append(Participant(name))
    return participants

def set_dead_participants(participants):
    with open('dead.txt', 'r') as f:
        while True:
            line = f.readline()
            if line == '':
                break
            name = line.replace('\n', '')
            print(name)
            participant = [participant for participant in participants if participant.name == name][0]
            participant.alive = False

def get_messages():
    return json.load(open('messages.json', 'r'))

class Queue:
    def __init__(self):
        self.list = []

    def log(self, msg, encounter_number, participants):
        print(f'[{encounter_number}] {msg}')
        with open(f'logs/{encounter_number}.txt', 'a') as f:
            f.write(msg + '\n')
        if participants is not None:
            img_path = f'logs/{encounter_number}.png'
            img = draw_participants(participants)
            img.save(img_path)

            self.list.append((msg, img_path, ))
            # tweet(msg, img_path)
        else:
            self.list.append((msg, ))
            # tweet(msg)

    def pop(self):
        if len(self.list) > 0:
            return self.list.pop(0)
        else:
            return None

game_finished = False

def main_thread(queue):
    participants = get_participants()
    set_dead_participants(participants)
    messages = get_messages()

    queue.log(messages['start'].format(len(participants)), -1, participants)

    encounter_duration = config['encounter_duration']
    encounter_delay = config['encounter_delay']

    i = 0
    alive_participants = [participant for participant in participants if participant.isalive()]
    while len(alive_participants) > 1:
        # Espera hasta que la hora esté entre las 12 y las 23, incluidas
        while not 12 <= dt.datetime.now().hour <= 23:
            print('.', end='', flush=True)
            sleep(10)
        p1, p2 = random.sample(alive_participants, 2)

        queue.log(messages['encounter'].format(p1.name, p2.name), i, participants=None)
        sleep(encounter_duration)

        p1_val = random.random()
        p2_val = random.random()

        if p1_val > p2_val:
            # P1 wins
            p2.kill()
            alive_participants = [participant for participant in participants if participant.isalive()]
            queue.log(messages['kill'].format(p1.name, p2.name, len(alive_participants)), i, participants)
        elif p1_val < p2_val:
            # P2 wins
            p1.kill()
            alive_participants = [participant for participant in participants if participant.isalive()]
            queue.log(messages['kill'].format(p2.name, p1.name, len(alive_participants)), i, participants)
        elif p1_val == p2_val:
            # Tie
            queue.log(messages['tie'].format(p1.name, p2.name, len(alive_participants)), i, participants)

        i += 1
        if len(alive_participants) == 1:
            break
        sleep(encounter_delay)
    queue.log(messages['win'].format(alive_participants[0].name), 'end', participants)

def tweeter_thread(queue):
    while True:
        item = queue.pop()
        if item is not None:
            tweeted = False
            while not tweeted:
                try:
                    if len(item) == 1:
                        tweet(item[0])
                        tweeted = True
                    elif len(item) == 2:
                        tweeted = tweet(item[0], item[1])
                        tweeted = True
                except TwythonError as e:
                    print('Twython Error')
                    print(e)
                    init_tweet()
                    tweeted = False

if __name__ == '__main__':
    init_tweet()
    tweet_queue = Queue()
    thread_main = threading.Thread(target=main_thread, args=(tweet_queue, ))
    thread_tweet = threading.Thread(target=tweeter_thread, args=(tweet_queue, ))
    thread_main.start()
    thread_tweet.start()
    # main()
