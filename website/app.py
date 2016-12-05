from flask import Flask
import requests
import jsonify
import random
app = Flask(__name__)

def last_xkcd():
    last_id = requests.get('http://xkcd.com/info.0.json')
    return int(last_id.json()['num'])

def gen_ran():
    return random.randrange(0, last_xkcd()+1)

@app.route("/")
def random_xkcd():
    rand_xkcd_img_url = requests.get('https://xkcd.com/{}/info.0.json'.format(gen_ran())) 
    rand_xkcd_img_url = rand_xkcd_img_url.json()['img']
    return "<img src=\"%s\">" % rand_xkcd_img_url

if __name__ == "__main__":
    app.run()