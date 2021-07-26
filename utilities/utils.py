import random
import re
import shutil
import csv
import requests
from difflib import SequenceMatcher

riddle_answer_pairs = []
current_riddle_answer = ""


def random_animal_emoji():
    emojis = [":frog:", ":pig:", ":rabbit:", ":dog:", ":cat:", ":mouse:", ":hamster:", ":fox:", ":bear:",
              ":panda_face:", ":hatching_chick:", ":chicken:", ":penguin:"]

    choice = random.choice(emojis)

    return choice


def random_8ball_response():
    responses = ["Yes", "No", "Maybe", "Certainly", "Surely not", "Of Course", "No way",
                 "Who Cares?", "Fo Sho Dawg", ":frog:"]
    choice = random.choices(responses, weights=[1, 1, 1, 1, 1, 1, 1, .5, .5, .05])[0]

    output = "_**" + choice + "**_"

    return output


async def add_to_list(new_line, guild):
    with open("lists/" + guild + "/list.txt", 'a') as file:
        file.writelines(new_line + "\n")


async def add_to_free_list(new_line, guild):
    with open("lists/" + guild + "/free_list.txt", 'a') as file:
        file.writelines(new_line + "\n")


async def list_all_lines(guild):
    with open("lists/" + guild + "/list.txt", 'r') as file:
        lines = list(enumerate(file.readlines()))

    lines = [item for sublist in lines for item in sublist]
    lines = list(map(str, lines))
    chunks = [lines[x:x+50] for x in range(0, len(lines), 50)]

    return chunks


async def list_all_free_lines(guild):
    with open("lists/" + guild + "/free_list.txt", 'r') as file:
        lines = list(enumerate(file.readlines()))

    lines = [item for sublist in lines for item in sublist]
    lines = list(map(str, lines))
    chunks = [lines[x:x + 50] for x in range(0, len(lines), 50)]

    return chunks


async def get_line(index, guild):
    with open("lists/" + guild + "/list.txt", "r") as infile:
        lines = infile.readlines()
    return lines[index]


async def get_free_line(index, guild):
    with open("lists/" + guild + "/free_list.txt", "r") as infile:
        lines = infile.readlines()
    return lines[index]


async def delete_line(index, guild):
    with open("lists/" + guild + "/list.txt", "r") as infile:
        lines = infile.readlines()

    if index <= len(lines):
        with open("lists/" + guild + "/list.txt", "w") as outfile:
            for pos, line in enumerate(lines):
                if pos != index:
                    outfile.write(line)


async def delete_free_line(index, guild):
    with open("lists/" + guild + "/free_list.txt", "r") as infile:
        lines = infile.readlines()

    if index <= len(lines):
        with open("lists/" + guild + "/free_list.txt", "w") as outfile:
            for pos, line in enumerate(lines):
                if pos != index:
                    outfile.write(line)


async def reset_list(guild):
    try:
        shutil.copy("lists/" + guild + "/list.txt", "lists/" + guild + "/list_OLD.txt")
    except Exception:
        print("There is no old list to backup. New server being initialised.")

    with open("./lists/default_list.txt", "r") as default_file:
        default_lines = default_file.readlines()

    with open("lists/" + guild + "/list.txt", "w") as file:
        for line in default_lines:
            file.write(line)


async def reset_free_list(guild):
    try:
        shutil.copy("lists/" + guild + "/free_list.txt", "lists/" + guild + "/free_list_OLD.txt")
    except Exception:
        print("There is no old list to backup. New server being initialised.")

    with open("./lists/default_free_list.txt", "r") as default_file:
        default_lines = default_file.readlines()

    with open("lists/" + guild + "/free_list.txt", "w") as file:
        for line in default_lines:
            file.write(line)


def load_riddles():
    global riddle_answer_pairs

    with open('./resources/riddles/more riddles.csv', 'r', encoding='utf-8') as read_obj:
        # pass the file object to reader() to get the reader object
        csv_reader = csv.reader(read_obj)
        # Get all rows of csv from csv_reader object as list of tuples
        list_of_tuples = list(map(tuple, csv_reader))
        riddle_answer_pairs = list_of_tuples

    print("riddles loaded!")

    return


async def random_riddle_answer():
    global current_riddle_answer

    pair = random.choice(riddle_answer_pairs)
    riddle, answer = str(pair[0]), str(pair[1])
    answer = answer.strip(" \"")
    out = "_" + riddle + "_" + "\n" + pad_spoiler_with_spaces(answer)

    current_riddle_answer = answer
    return out


async def check_riddle(text):
    global current_riddle_answer
    if SequenceMatcher(None, text.lower(), current_riddle_answer.lower()).ratio() > 0.8:
        return True
    else:
        return False


def random_wipe_reason(caller):
    reasons = ["Tank", "Off-Tank", "DPS", "Healer", "Yuki", "@" + caller, "🐸"]
    weights = [1, 1, 1, 1, 1, 1, 0.05]
    reason = random.choices(reasons, weights=weights)[0]
    if reason == "@" + caller:
        return "_It was the **" + "<" + reason + ">" + "**_"
    output = "_It was the **" + reason + "**_"
    return output


def yolo_response(img_url):
    DETECTION_URL = "http://localhost:5000/v1/object-detection/yolov5s"
    response = requests.post(DETECTION_URL, json={"image_url": img_url})

    if response.status_code == 200:
        img_path = "./yolo/out.jpg"
        return img_path
    return ""


def pad_spoiler_with_spaces(text):
    if len(text) < 10:
        for _ in range(10 - len(text)):
            text += " "
    out = "||" + text + "||"
    return out


def emoji_free_text(text):
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U0001F1F2-\U0001F1F4"  # Macau flag
                               u"\U0001F1E6-\U0001F1FF"  # flags
                               u"\U0001F600-\U0001F64F"
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               u"\U0001f926-\U0001f937"
                               u"\U0001F1F2"
                               u"\U0001F1F4"
                               u"\U0001F620"
                               u"\u200d"
                               u"\u2640-\u2642"
                               "]+", flags=re.UNICODE)

    text = emoji_pattern.sub(r'', text)
    return text


def analyze_tea_fight(log_id, api_key):
    response = requests.get(f"https://www.fflogs.com:443/v1/report/fights/{log_id}?api_key={api_key}")

    if response.status_code != 200:
        return None

    tea_fights = [fight for fight in response.json()['fights'] if fight['boss'] == 1050]

    if len(tea_fights) == 0:
        return None

    def get_deaths():
        last_fight = tea_fights[-1]
        death_reponse = requests.get(f"https://www.fflogs.com:443/v1/report/events/deaths/{log_id}?end={last_fight['end_time']}&api_key={api_key}")

        if death_reponse.status_code != 200:
            return None
        
        party_member_deaths = [death for death in death_reponse.json()['events'] if death['targetIsFriendly'] == True]
        
        death_counts = {}
        for death in party_member_deaths:
            killing_ability = death.get('killingAbility')
            killing_ability_name = "Suicide" if killing_ability is None else death['killingAbility']['name']
            if death_counts.get(killing_ability_name) is not None:
                death_counts[killing_ability_name] = death_counts[killing_ability_name] + 1
            else:
                death_counts[killing_ability_name] = 1
        
        return death_counts

    embolus = [enemy for enemy in response.json()['enemies'] if enemy['name'] == "Embolus"]
    embolus_wipes = len(embolus[0]['fights']) if len(embolus) == 1 else 0

    fight_id = 1
    active_time = 0

    for fight in tea_fights:
        fight["id"] = fight_id
        fight_id += 1

        active_time = active_time + fight["end_time"]/1000 - fight["start_time"]/1000

    def get_phase_count(phase):
        return len([fight for fight in tea_fights if fight['lastPhaseForPercentageDisplay'] == phase])
    best_fight = min(tea_fights, key=lambda f: f['fightPercentage'])
    return {
        "total": len(tea_fights),
        "phase1": get_phase_count(1),
        "phase2": get_phase_count(2),
        "phase3": get_phase_count(3),
        "phase4": get_phase_count(4),
        "active_time": active_time,
        "embolus_wipes": embolus_wipes,
        "best_fight": {
            "id": best_fight["id"],
            "length": (best_fight["end_time"] - best_fight["start_time"])/1000,
            "fightPercentage": 100 - best_fight['fightPercentage']/100,
            "currentPhaseProg": 100 - best_fight['bossPercentage']/100
        },
        "death_counts": get_deaths()
    }
