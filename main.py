import os

import requests
from flask import Flask, send_file, Response
from bs4 import BeautifulSoup

app = Flask(__name__)


def get_fact():

    response = requests.get("http://unkno.com")

    soup = BeautifulSoup(response.content, "html.parser")
    facts = soup.find_all("div", id="content")

    return facts[0].getText()

@app.route('/')
def home():
    fact = get_fact()
    url = 'https://hidden-journey-62459.herokuapp.com/piglatinize/'


    # apparently don't allow redirects. Magic.
    response = requests.post(url, data = {'input_text': fact}, allow_redirects = False)

    urlloc = response.headers['Location']
    
    # return urlloc

    response = requests.get("{}".format(urlloc))

    soup = BeautifulSoup(response.content, features="html.parser")


    # Maybe change this so it's only the quote? But whatever, I'm okay with the full body.
    quote = soup.find("body")

    return quote.getText()


# return location_header

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6787))
    app.run(host='0.0.0.0', port=6787)
