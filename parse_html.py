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

def parse_html(file_path, sys_name, user_name, window_size=5, max_overlap=2):
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

        # Append Conversation
        conversations.append({
            "from": "gpt" if speaker == sys_name else "human",
            "value": text
        })

        # Append to data if window is reached
        if curr == end:
            data.append({
                "id": len(data),
                "conversations": conversations
            })
            conversations = []
            curr = end - max_overlap
            end = curr + window_size
        else:
            curr += 1
    return data

if __name__ == "__main__":
    dataset = parse_html(FILE_PATH, SYS_NAME, USER_NAME)
    pprint(dataset)
    with open("transcript_json/0.json", "w") as file:
        json.dump(dataset, file, indent=4)
