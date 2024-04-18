import os
import json
from dotenv import load_dotenv
from openai import AzureOpenAI

load_dotenv()

client = AzureOpenAI()

def complete_summary(transcript):
    completion = client.chat.completions.create(
        model=os.environ.get("AZURE_OPENAI_CHAT_DEPLOYMENT"),
        messages=[
            {"role": "system", "content": "You are a assistant in help summarizing a conversation between a patient and an therapist.\nSummarize consizly into 2 or 3 sentences.\n The conversations are in json format."},
            {"role": "user", "content": transcript}
        ]
    )
    return completion.choices[0].message.content

def load_transcript(file):
    with open(file, "r") as file:
        data = json.load(file)
    return data

def append_to_json_file(file_path, data):
    with open(file_path, 'r') as file:
        try:
            existing_data = json.load(file)
        except json.decoder.JSONDecodeError:
            existing_data = []
        
    # Append new data to the existing data
    existing_data.append(data)
        
    # Write the data to the file
    with open(file_path, 'w') as file:
        json.dump(existing_data, file, indent=4)

def store_summary(transcript, file_path):
    summary = complete_summary(json.dumps(transcript))
    data_to_store = {
        "transcript": transcript,
        "summary": summary
    }
    append_to_json_file(file_path, data_to_store)

if __name__ == "__main__":
    transcript = load_transcript("transcript_json/sequential.json")
    store_summary(transcript[0:20], "transcript_json/summary.json")
