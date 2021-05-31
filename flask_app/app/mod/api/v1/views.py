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
    text = text.lower()
    print(request.json)
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

    sen = re.split(r"(press \d|pound|one|two|three|four|five|six|seven|eight|nine|zero)",text.lower())
    try:
        for i in range(len(sen)):
            temp = {}
            if "english" in sen[i] :
                value = getno.findall(sen[i+1]) 
                if value:
                    temp = {}
                    temp["command"] = "DTMF" 
                    temp["value"] = strtoint.get(value[0])
                    response['action'].append(temp)
            elif userdetails['lname'] in sen[i] or userdetails['fname'] in sen[i]:
                if userdetails['lname'] in sen[i] and userdetails['fname'] in sen[i]:
                    temp = {}
                    temp['command'] = "hangup"
                    temp['value'] = True
                    temp['varified'] = True
                    response['action'].append(temp)
                elif "is that correct" in sen[i]:
                    temp = {}
                    temp["command"] = "play" 
                    temp["value"] = "yes"
                    response['action'].append(temp)
                else:
                    value = getno.findall(sen[i+1]) 
                    if value:
                        temp = {}
                        temp["command"] = "DTMF" 
                        temp["value"] = strtoint.get(value[0])
                        response['action'].append(temp)
            elif "say" in sen[i] :
                if "last and first" in sen[i] or "last name first" in sen[i] :
                    temp["command"] = "play"
                    temp["value"] = f"{userdetails['lname']} {userdetails['fname']}"
                    response['action'].append(temp)
                    if "pound" in sen[i+1] :
                        temp = {}
                        temp["command"] = "DTMF" 
                        temp["value"] = "#"
                        response['action'].append(temp)
                elif "first and last" in sen[i] or "1st and last" in sen[i] :
                    temp["command"] = "play"
                    temp["value"] = f"{userdetails['fname']} {userdetails['lname']}"
                    response['action'].append(temp)
                    if "pound" in sen[i+1]:
                        temp = {}
                        temp["command"] = "DTMF" 
                        temp["value"] = "#"
                        response['action'].append(temp)
                elif "first name" in sen[i]:
                    temp["command"] = "play"
                    temp["value"] = f"{userdetails['fname']}"
                    response['action'].append(temp)
                    if "pound" in sen[i+1]:
                        temp = {}
                        temp["command"] = "DTMF" 
                        temp["value"] = "#"
                        response['action'].append(temp)
                elif "last name" in sen[i]:
                    temp["command"] = "play"
                    temp["value"] = f"{userdetails['lname']}"
                    response['action'].append(temp)
                    if "pound" in sen[i+1]:
                        temp = {}
                        temp["command"] = "DTMF" 
                        temp["value"] = "#"
                        response['action'].append(temp)
                elif "name" in sen[i]:
                    temp["command"] = "play"
                    temp["value"] = f"{userdetails['fname']} {userdetails['lname']}"
                    response['action'].append(temp)
                    value = getno.findall(sen[i+1]) 
                    if value:
                        temp = {}
                        temp["command"] = "DTMF" 
                        temp["value"] = strtoint.get(value[0])
                        response['action'].append(temp)
            elif "directory" in sen[i]:
                if "to access our staff directory" in sen[i] or "to consult our directory" in sen[i]:
                    value = getno.findall(sen[i-1])
                else:
                    value = getno.findall(sen[i+1])
                if value:
                    temp["command"] = "DTMF"
                    temp["value"] = strtoint.get(value[0])
                    response['action'].append(temp)
            elif "spell" in sen[i] or "enter" in sen[i] or "know" in sen[i]:
                if "last and first" in sen[i] or "last name and first" in sen[i] or "last name first name" in sen[i] or "last in first name" in sen[i] or "last name and then spell the first name" in sen[i] or "last name first" in sen[i]:
                    try:
                        temp = {}
                        temp["command"] = "DTMF_string"
                        temp["value"] = f"{userdetails['lname']} {userdetails['fname']}#" if "pound" in sen[i+1] or "followed by number sign" in sen[i] else f"{userdetails['lname']} {userdetails['fname']}"
                        response['action'].append(temp)
                    except Exception as e:
                        print(e)
                    finally:
                        temp = {}
                        temp["command"] = "DTMF_string"
                        temp["value"] = f"{userdetails['lname']} {userdetails['fname']}"
                        response['action'].append(temp)
                elif "first and last" in sen[i] or "first name and last" in sen[i]:
                    try:
                        temp = {}
                        temp["command"] = "DTMF_string"
                        temp["value"] = f"{userdetails['fname']} {userdetails['lname']}#" if "pound" in sen[i+1] or "followed by number sign" in sen[i] else f"{userdetails['fname']} {userdetails['lname']}"
                        response['action'].append(temp)
                    except Exception as e:
                        print(e)
                    finally:
                        temp = {}
                        temp["command"] = "DTMF_string"
                        temp["value"] = f"{userdetails['fname']} {userdetails['lname']}"
                        response['action'].append(temp)
                elif "first name" in sen[i]:
                    try:
                        temp = {}
                        temp["command"] = "DTMF_string"
                        temp["value"] = f"{userdetails['fname']}#" if "pound" in sen[i+1] or "followed by number sign" in sen[i] else f"{userdetails['fname']}"
                        response['action'].append(temp)
                    except Exception as e:
                        print(e)
                    finally:
                        temp = {}
                        temp["command"] = "DTMF_string"
                        temp["value"] = f"{userdetails['fname']}"
                        response['action'].append(temp)
                elif "last name" in sen[i] or "last name first" in sen[i]:
                    if "last name and" in sen[i] and "pound" in sen[i+1]:
                        temp = {}
                        temp["command"] = "DTMF_string"
                        temp["value"] = f"{userdetails['lname']}#"
                        response['action'].append(temp)
                    else:
                        value = getno.findall(sen[i+1]) 
                        if value and "at least" not in sen[i]:
                            temp = {}
                            temp["command"] = "DTMF" 
                            temp["value"] = strtoint.get(value[0])
                            response['action'].append(temp)
                        else:
                            try:
                                temp = {}
                                temp["command"] = "DTMF_string"
                                temp["value"] = f"{userdetails['lname']}#" if "pound" in sen[i+1] or "followed by number sign" in sen[i] else f"{userdetails['lname']}"
                                response['action'].append(temp)
                            except Exception as e:
                                print(e)
                            finally:
                                temp = {}
                                temp["command"] = "DTMF_string"
                                temp["value"] = f"{userdetails['lname']}"
                                response['action'].append(temp)
                elif "name" in sen[i]:
                    value = getno.findall(sen[i+1]) 
                    if value:
                        temp = {}
                        temp["command"] = "DTMF" 
                        temp["value"] = strtoint.get(value[0])
                        response['action'].append(temp)
            elif "you like to reach" in sen[i]:
                temp = {}
                temp["command"] = "play"
                temp["value"] = f"{userdetails['fname']} {userdetails['lname']}"
                response['action'].append(temp)
            elif "dial by name" in sen[i] or "dial by last name" in sen[i]:
                if "to dial by" in sen[i]:
                    value = getno.findall(sen[i-1])
                else:
                    value = getno.findall(sen[i+1]) if i+1 < len(sen) else getno.findall(sen[i-1])
                if value:
                    temp = {}
                    temp["command"] = "DTMF" 
                    temp["value"] = strtoint.get(value[0])
                    response['action'].append(temp)
            elif "last name" in sen[i]:
                value = getno.findall(sen[i+1]) 
                if value:
                    temp = {}
                    temp["command"] = "DTMF" 
                    temp["value"] = strtoint.get(value[0])
                    response['action'].append(temp)
            elif "transferring" in sen[i] or ("wait while i transfer your call" in sen[i] and "operator" not in sen[i]) or "being transferred please hold" in sen[i] or "please hold while I try to connect you" in sen[i]:
                temp = {}
                temp['command'] = "hangup"
                temp['value'] = True
                temp['varified'] = True
                response['action'].append(temp)
            elif "hear the next name" in sen[i]:
                value = getno.findall(sen[i+1]) 
                if value:
                    temp = {}
                    temp["command"] = "DTMF" 
                    temp["value"] = strtoint.get(value[0])
                    response['action'].append(temp)
            elif "is not available record your message" in sen[i] or "not finding a match for that name" in sen[i]:
                temp = {}
                temp["command"] = "hangup" 
                temp["value"] = True
                temp['varified'] = False
                temp["comment"] = "name not recognised"
                response['action'].append(temp)
    except Exception as e:
        print(e)
    finally : 
        print(response)
        return jsonify(response)
