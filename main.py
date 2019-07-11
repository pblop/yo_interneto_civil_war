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

def log(msg, encounter_number, participants):
    print(f'[{encounter_number}] {msg}')
    with open(f'logs/{encounter_number}.txt', 'a') as f:
        f.write(msg + '\n')
    if participants is not None:
        img_path = f'logs/{encounter_number}.png'
        img = draw_participants(participants)
        img.save(img_path)

        tweet(msg, img_path)
    else:
        tweet(msg)

def main():
    participants = get_participants()
    print(len(participants))
    messages = get_messages()

    log(messages['start'].format(len(participants)), -1, participants)

    encounter_duration = config['encounter_duration']
    encounter_delay = config['encounter_delay']
    i = 0
    alive_participants = [participant for participant in participants if participant.isalive()]
    while len(alive_participants) > 1:
        p1, p2 = random.sample(alive_participants, 2)

        log(messages['encounter'].format(p1.name, p2.name), i, participants=None)
        sleep(encounter_duration)

        p1_val = random.random()
        p2_val = random.random()

        if p1_val > p2_val:
            # P1 wins
            p2.kill()
            alive_participants = [participant for participant in participants if participant.isalive()]
            log(messages['kill'].format(p1.name, p2.name, len(alive_participants)), i, participants)
        elif p1_val < p2_val:
            # P2 wins
            p1.kill()
            alive_participants = [participant for participant in participants if participant.isalive()]
            log(messages['kill'].format(p2.name, p1.name, len(alive_participants)), i, participants)
        elif p1_val == p2_val:
            # Tie
            log(messages['tie'].format(p1.name, p2.name, len(alive_participants)), i, participants)

        i += 1
        sleep(encounter_delay)

    log(messages['win'].format(alive_participants[0].name), 'end', participants)

if __name__ == '__main__':
    main()
