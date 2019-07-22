import json
import random
from tweet import tweet
from generate_image import draw_participants
from enum import Enum
from time import sleep

config = json.load(open('./config.json', 'r'))

class Participant:
    def __init__(self, name):
        self.name = name
        self.alive = True

    def isalive(self):
        return self.alive

    def kill(self):
        self.alive = False

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

def get_messages():
    return json.load(open('messages.json', 'r'))

def main():
    participants = get_participants()

    img = draw_participants(participants)
    img.save('participants.png')


if __name__ == '__main__':
    main()
