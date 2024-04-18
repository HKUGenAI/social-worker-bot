from bs4 import BeautifulSoup
from pprint import pprint
import json
import re

FILE_PATH = "transcript_html/0.html"
SYS_NAME = "Dr. Ali Marsh"
USER_NAME = "Julia"

def get_soup(file_path):
    with open(file_path, "r") as file:
        soup = BeautifulSoup(file, "html.parser")
        return soup

def parse_html_sliding_window(file_path, sys_name, user_name, window_size=8, max_overlap=4):
    data = []
    curr = 0
    end = curr + window_size
    soup = get_soup(file_path)
    tags = soup.select("p.transp")
    conversations = []
    while curr < len(tags):
        # Get speaker
        speaker = tags[curr].find("span", class_="speaker")
        if speaker == None:
            curr += 1
            end += 1
            continue
        speaker = speaker.text.strip()

        # Ensure conversation initiated by human
        if curr == end - window_size and speaker == sys_name:
            curr += 1
            end += 1
            continue

        # Get text
        text = tags[curr].find_all("span", class_="transspan")
        text = "".join([re.sub('(\u00a0|\n)\s*', ' ', t.text) for t in text[1:]]).strip()

        actor = "gpt" if speaker == sys_name else "human"

        # Append Conversation
        if conversations != [] and actor == conversations[-1]["from"]:
            conversations[-1]["value"] += " " + text
            end += 1
        else:
            conversations.append({
                "from": actor,
                "value": text
            })

        curr += 1
        # Append to data if window is reached
        if curr == end:
            data.append({
                "id": len(data),
                "conversations": conversations
            })
            print(len(data))
            conversations = []
            curr = end - max_overlap
            end = curr + window_size
 
    return data

def parse_html_sequential(file_path, sys_name, user_name, window_size=8, max_overlap=4):
    curr = 0
    soup = get_soup(file_path)
    tags = soup.select("p.transp")
    conversations = []
    while curr < len(tags):
        # Get speaker
        speaker = tags[curr].find("span", class_="speaker")
        if speaker == None:
            curr += 1
            continue
        speaker = speaker.text.strip()

        # Get text
        text = tags[curr].find_all("span", class_="transspan")
        text = "".join([re.sub('(\u00a0|\n)\s*', ' ', t.text) for t in text[1:]]).strip()

        actor = "gpt" if speaker == sys_name else "human"

        # Append Conversation
        if conversations != [] and actor == conversations[-1]["from"]:
            conversations[-1]["value"] += " " + text
        else:
            conversations.append({
                "from": actor,
                "value": text
            })

        curr += 1
 
    return conversations


if __name__ == "__main__":
    dataset = parse_html_sequential(FILE_PATH, SYS_NAME, USER_NAME)
    pprint(dataset)
    with open("transcript_json/sequential.json", "w") as file:
        json.dump(dataset, file, indent=4)
