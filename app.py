# doing necessary imports
from flask import Flask, render_template, request, jsonify, make_response
from flask_cors import CORS, cross_origin
import requests
import pymongo
import json
import os
from Conversations import *
#from DataRequests import MakeApiRequests
#from sendEmail import EMailClient
from pymongo import MongoClient

app = Flask(__name__)  # initialising the flask app with the name 'app'


# geting and sending response to dialogflow
@app.route('/webhook', methods=['POST'])
@cross_origin()
def webhook():
    req = request.get_json(silent=True, force=True)
    res = processRequest(req)
    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


# processing the request from dialogflow
def processRequest(req):
    # dbConn = pymongo.MongoClient("mongodb://localhost:27017/")  # opening a connection to Mongo
    log = Log.saveConversations()
    sessionID = req.get('responseId')
    result = req.get("queryResult")
    intent = result.get("intent").get('displayName')
    query_text = result.get("queryText")
    parameters = result.get("parameters")
    cust_name = parameters.get("cust_name")
    cust_contact = parameters.get("cust_contact")
    cust_email = parameters.get("cust_email")
    db = configureDataBase()


    if intent == "confirmation":
        fulfillmentText = result.get("fulfillmentText")
        log.saveConversations(sessionID, query_text, fulfillmentText, intent, db)
    elif intent == "Continue":
        fulfillmentText = result.get("fulfillmentText")
        log.saveConversations(sessionID, query_text, fulfillmentText, intent, db)

    elif intent == "Welcome" or intent== "fallback":
        fulfillmentText = result.get("fulfillmentText")
        log.saveConversations(sessionID, query_text, fulfillmentText, intent, db)



    else:
        return {
            "fulfillmentText": "something went wrong,Lets start from the begning, Say Hi",
        }


def configureDataBase():
    client = MongoClient("mongodb+srv://chatwithnerd:password@cluster0.rbm6q.mongodb.net/shravan?retryWrites=true&w=majority")
    return client.get_database('shravan')


'''def makeAPIRequest(query):
    api = MakeApiRequests.Api()

    if query == "world":
        return api.makeApiWorldwide()
    if query == "state":
        return api.makeApiRequestForIndianStates()

    else:
        return api.makeApiRequestForCounrty(query)'''



if __name__ == '__main__':
    port = int(os.getenv('PORT'))
    print("Starting app on port %d" % port)
    app.run(debug=False, port=port, host='0.0.0.0')
'''if __name__ == "__main__":
    app.run(port=5000, debug=True)''' # running the app on the local machine on port 8000
