import os
import json
import requests
from flask import Blueprint, request, jsonify
import re
from app import logging

logger = logging.getLogger(__name__)

blueprint_flask = Blueprint("flask", __name__)

@blueprint_flask.route("/predict", methods=["POST"])
def predict():
    text = request.json.get("text")
    userdetails = request.json.get("userdetails")
    callid = request.json.get('callid')

    response = {
                "text": text,
                "callid": callid,
                "userdetails": userdetails,
                "action" : []
            }
    getno = re.compile('(one|two|three|four|five|six|seven|eight|nine|\d|pound)')
    strtoint = {
                "one":1,
                "two":2,
                "three":3,
                "four":4,
                "five":5,
                "six":6,
                "seven":7,
                "eight":8,
                "nine":9,
                "pound":"#",
                '1':1,
                '2':2,
                '3':3,
                '4':4,
                '5':5,
                '6':6,
                '7':7,
                '8':8,
                '9':9
            }
    for i in text.split("."):
        temp = {}
        if "directory" in i:
            value = getno.findall(i)
            if value:
                temp["command"] = "DTMF"
                temp["value"] = strtoint.get(value[0])
                response['action'].append(temp)
        elif "spell" in i:
            if "last and first" in i :
                temp["command"] = "DTMF"
                temp["value"] = f"{userdetails['Lname']}{userdetails['Fname']}"
                response['action'].append(temp)
                if "pound" in i:
                    temp = {}
                    temp["command"] = "DTMF"
                    temp["value"] = "#"
                    response['action'].append(temp)
            elif "first and last" in i:
                temp["command"] = "DTMF"
                temp["value"] = f"{userdetails['Fname']}{userdetails['Lname']}"
                response['action'].append(temp)
                if "pound" in i:
                    temp = {}
                    temp["command"] = "DTMF"
                    temp["value"] = "#"
                    response['action'].append(temp)
            elif "first name" in i:
                temp["command"] = "DTMF"
                temp["value"] = f"{userdetails['Fname']}"
                response['action'].append(temp)
                if "pound" in i:
                    temp = {}
                    temp["command"] = "DTMF"
                    temp["value"] = "#"
                    response['action'].append(temp)
            elif "last name" in i:
                temp["command"] = "DTMF"
                temp["value"] = f"{userdetails['Lname']}"
                response['action'].append(temp)
                if "pound" in i:
                    temp = {}
                    temp["command"] = "DTMF"
                    temp["value"] = "#"
                    response['action'].append(temp)
        elif "last name" in i:
            value = getno.findall(i)
            if value:
                temp = {}
                temp["command"] = "DTMF"
                temp["value"] = strtoint.get(value[0])
                response['action'].append(temp)
        elif userdetails['Lname'] in i or userdetails['Fname'] in i:
            value = getno.findall(i)
            print(value)
            if value:
                temp = {}
                temp["command"] = "DTMF"
                temp["value"] = strtoint.get(value[0])
                response['action'].append(temp)
        elif "english" in i:
            value = getno.findall(i)
            if value:
                temp["command"] = "DTMF"
                temp["value"] = strtoint.get(value[0])
                response['action'].append(temp)
                
    return jsonify(response)
