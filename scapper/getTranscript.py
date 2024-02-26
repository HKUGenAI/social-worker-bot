import requests
import json
import pprint
from bs4 import BeautifulSoup
from requests_html import HTMLSession
s = HTMLSession()

def getTranscript(url, uid, pin):
    # Get the page content
    print("Requesting: " + url)
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')

    # HKU Lib Login required
    if soup.title.string == "Shibboleth Authentication Request":
        # Get required post url
        form = soup.find(name='form')
        post_url = form.get('action')
        print(s.cookies)

        # Get required post payloads
        post_payload = {}
        input_tags = soup.find_all('input') 
        for tag in input_tags: 
            if tag.get('name') == 'RelayState':
                post_payload['RelayState'] = tag.get('value')
            elif tag.get('name') == 'SAMLRequest':
                post_payload['SAMLRequest'] = tag.get('value')

        # Post request to authentication page
        print("Requesting authentication page...")
        r = s.post(post_url, data=post_payload, cookies=s.cookies)
        r.html.render()
        print(r.headers)

        # Get required login url and payloads
        form = r.html.find("#hkulauth", first=True)
        post_url = form.attrs['action']
        soup = BeautifulSoup(form.html, 'html.parser')
        post_payload = {}
        for tag in soup.find_all('input'):
            if tag.get('value') != None:
                post_payload[tag.get('name')] = tag.get('value')
        post_payload['userid'] = uid
        post_payload['password'] = pin
        # pprint.pprint(post_payload)

        # Post request to login
        print("Logging in...")
        r = s.post(post_url, data=post_payload, cookies=s.cookies, verify=False)
        # r.html.render()
        print(r.headers)
        print(r.html)

        soup = BeautifulSoup(r.content, 'html.parser')
        print(soup.prettify())



if __name__ == "__main__":
    with open('videoList.json', 'r') as file:
            data = json.load(file)
    url = data[0]
    getTranscript(url, '', '')