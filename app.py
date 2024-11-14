from app import app
from flask import Flask,render_template,request,flash,redirect
import requests
from urllib.parse import quote_plus
from pymongo import MongoClient
from service import check_voters,add_voter
import json
import datetime
CONNECTED_SERVICE_ADDRESS = "http://127.0.0.1:8000"
import os

start = Flask(__name__)

#if using mongodb
# from dotenv import load_dotenv
# load_dotenv()
# password =  os.getenv('DB_PASS')
# conn_str = os.getenv('CONN_STR')
# POLITICAL_PARTY_IDS = []
# POLITICAL_PARTY_NAMES = []
# client = MongoClient(conn_str)
# db = client["electionDB"]
# party_collection = db["party"]

# for party in party_collection.find({}, {"party_name": 1, "party_id": 1, "_id": 0}):
#         POLITICAL_PARTY_NAMES.append(party.get("party_name"))
#         POLITICAL_PARTY_IDS.append(party.get("party_id"))


POLITICAL_PARTY_NAMES=["Democratic Party","National Party","State Party"]
POLITICAL_PARTY_IDS=["Ni67lat","ya48jiv","Spe55ma"]
PARTIES = zip(POLITICAL_PARTY_NAMES,POLITICAL_PARTY_IDS)
posts = []

@start.route("/admin_panel",methods=["GET"])
def admin():
    fetch_posts()

    vote_gain = []
    for post in posts:
        vote_gain.append(post["party"])
    print(f"posts -> {posts}")
    return render_template('admin.html',
                           posts=posts,
                           vote_gain=vote_gain,
                           readable_time=timestamp_to_string,
                           political_parties=POLITICAL_PARTY_NAMES)

def timestamp_to_string(epoch_time):
    return datetime.datetime.fromtimestamp(epoch_time).strftime('%Y-%m-%d %H:%M')

def fetch_posts():
    """
    Function to fetch the chain from a blockchain node, parse the
    data and store it locally.
    """
    get_chain_address = "{}/chain".format(CONNECTED_SERVICE_ADDRESS)
    response = requests.get(get_chain_address)
    if response.status_code == 200:
        content = []
        vote_count = []
        chain = json.loads(response.content)
        for block in chain["chain"]:
            for tx in block["transactions"]:
                tx["index"] = block["index"]
                tx["hash"] = block["previous_hash"]
                content.append(tx)


        global posts
        posts = sorted(content, key=lambda k: k['timestamp'],
                       reverse=True)





# # def get_party_details():
# #     client = MongoClient(conn_str)
# #     db = client["electionDB"]
# #     party_collection = db["party"]

#     for party in party_collection.find({}, {"party_name": 1, "party_id": 1, "_id": 0}):
#         POLITICAL_PARTY_NAMES.append(party.get("party_name"))
#         POLITICAL_PARTY_IDS.append(party.get("party_id"))


@start.route('/',methods=['GET'])
def home():
    start.secret_key = '6dbf23122cb5046cc5c0c1b245c75f8e43c59ca8ffeac292715e5078e631d0c9'
    start.config['SESSION_TYPE'] = 'filesystem'
    return render_template('index.html',error=False)


@start.route('/',methods=['POST'])
def login():
    app_id = request.form['id']
    voter_name = request.form['name']
    if app_id=='shreeja':
        return redirect('/admin_panel')
    # client = MongoClient(conn_str)
    # db = client["electionDB"]
    # voters_collection = db.voters
    # voter = voters_collection.find_one({
    #     "app_id": app_id,
    #     "voters_name": voter_name
    # })
    voter=True
    if voter:
        return redirect('/home')
    else:
        return render_template('index.html',error=True)


@start.route('/home',methods=['GET'])
def vote_page():
    
    return render_template('home.html',parties = PARTIES,error=False,message="")




def check_party(curr_pid):
    # # client = MongoClient(conn_str)
    # # db = client["electionDB"]
    # # party_collection = db["party"]
    # # party = party_collection.find_one({
    # #     "party_id": curr_pid
    # # })
    # if party:
    #     return party['party_name']
    # return False
    ind = POLITICAL_PARTY_IDS.index(curr_pid)
    return POLITICAL_PARTY_NAMES[ind]
def check_voter(curr_vid):
    # client = MongoClient(conn_str)
    # db = client["electionDB"]
    # voters_collection = db["voters"]
    # verify = voters_collection.find_one({
    #     "voter_id": curr_vid
    # })
    # if verify:
    #     return True
    # return False
    return True

@start.route('/submit', methods=['POST'])
def submit_textarea():

    party = request.form["party"]
    voter_id = request.form["voter_id"]
    parrty_n = check_party(party)
    post_object = {
        'voter_id': voter_id,
        'party': parrty_n,
        'party_id':party,
    }

    
    if parrty_n and check_voter(voter_id):
        if check_voters(voter_id):
            print("already voted")
            return render_template('home.html',error=True,message="Already Voted..",parties = PARTIES)
        else:
            add_voter(voter_id)
            print("voter check successfully")
            new_tx_address = "{}/new_transaction".format(CONNECTED_SERVICE_ADDRESS)
            requests.post(new_tx_address,
                  json=post_object,
                  headers={'Content-type': 'application/json'})
            
            mine_address = "{}/mine".format(CONNECTED_SERVICE_ADDRESS)
            requests.get(mine_address)
            return render_template('home.html',error=False,message="Voted Successfully",parties = PARTIES)


    else:
        return render_template('home.html',error=True,message="Invalid Submission",parties = PARTIES)


if __name__ == '__main__':   
   start.run()