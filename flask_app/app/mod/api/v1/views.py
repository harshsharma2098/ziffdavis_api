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
    getno = re.compile('(one|two|three|four|five|six|seven|eight|nine|\\d|pound)')
    strtoint = {
                "zero":0,
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
                'star':"*",
                '0':0,
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

    sen = re.split(r"(press (\d|pound|one|two|three|four|five|six|seven|eight|nine|zero|star))",text.lower())
    print("*****************Complete sentence *****************")
    print(sen)
    print("*******Length of Sentence*********",len(sen))
    try:
        for i in range(len(sen)):
            temp = {}
            if "english" in sen[i] :
                print("*"*20)
                print("Line 55 condition : if english found in sen[i]")
                value = getno.findall(sen[i+1]) if i+1 <= len(sen) else None
                if value:
                    temp = {}
                    temp["command"] = "DTMF" 
                    temp["value"] = strtoint.get(value[0])
                    response['action'].append(temp)
            elif userdetails['lname'].lower() in sen[i].split() or userdetails['fname'].lower() in sen[i].split():
                print("*"*20)
                print("Line 64 condition : If lname or fname found in sen[i]")
                
                # if "record your message" in sen[i] or "not available" in sen[i] or "unavailable" in sen[i]:
                #     temp = {}
                #     temp['command'] = "hangup"
                #     temp['value'] = True
                #     temp['varified'] = True
                #     response['action'].append(temp)
                if userdetails['lname'].lower() in sen[i] and userdetails['fname'].lower() in sen[i]:
                    print("*"*20)
                    print("Line 73 condition : If lname and fname found in sen[i]")
                    temp = {}
                    temp['command'] = "hangup"
                    temp['value'] = True
                    temp['varified'] = True
                    response['action'].append(temp)
                # elif "is that correct" in sen[i]:
                #     temp = {}
                #     temp["command"] = "play" 
                #     temp["value"] = "yes"
                #     response['action'].append(temp)
                else:
                    # value = getno.findall(sen[i+1]) if i+1 <= len(sen) else None 
                    # if value:
                    #     temp = {}
                    #     temp["command"] = "DTMF" 
                    #     temp["value"] = strtoint.get(value[0])
                    #     response['action'].append(temp)
                    print("*"*20)
                    print("Line 86 condition : otherwise hangup and pass partial verify")
                    temp = {}
                    temp['command'] = "hangup"
                    temp['value'] = True
                    temp['partial_verify'] = True
                    response['action'].append(temp)
                    
            elif "say" in sen[i] :
                if "last and first" in sen[i] or "last name first" in sen[i] :
                    print("*"*20)
                    print("Line 101 condition : 'last and first' or 'last name first' in sen[i]")
                    temp["command"] = "play"
                    temp["value"] = f"{userdetails['lname']} {userdetails['fname']}"
                    response['action'].append(temp)
                    if "pound" in sen[i+1] :
                        print("*"*20)
                        print("Line 107 condition : If pound in sen[i+1] ")
                        temp = {}
                        temp["command"] = "DTMF" 
                        temp["value"] = "#"
                        response['action'].append(temp)
                elif "first and last" in sen[i] or "1st and last" in sen[i] :
                    print("*"*20)
                    print("Line 247 condition : 'first and last' in sen[i] or '1st and last' in sen[i] ")
                    temp["command"] = "play"
                    temp["value"] = f"{userdetails['fname']} {userdetails['lname']}"
                    response['action'].append(temp)
                    if "pound" in sen[i+1]:
                        print("*"*20)
                        print("Line 120 condition : pound in sen[i+1] ")
                        temp = {}
                        temp["command"] = "DTMF" 
                        temp["value"] = "#"
                        response['action'].append(temp)
                elif "first name" in sen[i]:
                    print("*"*20)
                    print("Line 128 condition : first name in sen[i] ")                    
                    temp["command"] = "play"
                    temp["value"] = f"{userdetails['fname']}"
                    response['action'].append(temp)
                    if "pound" in sen[i+1]:
                        print("*"*20)
                        print("Line 135 condition : pound in sen[i+1]")
                        temp = {}
                        temp["command"] = "DTMF" 
                        temp["value"] = "#"
                        response['action'].append(temp)
                elif "last name" in sen[i]:
                    print("*"*20)
                    print("Line 142 condition : last name in sen[i]")
                    temp["command"] = "play"
                    temp["value"] = f"{userdetails['lname']}"
                    response['action'].append(temp)
                    if "pound" in sen[i+1]:
                        print("*"*20)
                        print("Line 148 condition : pound in sen[i+1]")
                        temp = {}
                        temp["command"] = "DTMF" 
                        temp["value"] = "#"
                        response['action'].append(temp)
                
                elif "name" in sen[i]:
                    print("*"*20)
                    print("Line 155 condition : name in sen[i]")                    
                    temp["command"] = "play"
                    temp["value"] = f"{userdetails['fname']} {userdetails['lname']}"
                    response['action'].append(temp)
                    value = getno.findall(sen[i+1]) if i+1 <= len(sen) else None 
                    if value:
                        print("*"*20)
                        print("Line 163 condition : If value found")
                        temp = {}
                        temp["command"] = "DTMF" 
                        temp["value"] = strtoint.get(value[0])
                        response['action'].append(temp)
                elif "who would you like to reach" in sen[i] and "say" in sen[i]:
                    temp["command"] = "play"
                    temp["value"] = f"{userdetails['fname']} {userdetails['lname']}"
                    response['action'].append(temp)
            
            elif "name not found. enter last name and pound sign." in sen[i] or "name not found. enter last name and pound key." in sen[i] or "there were no matches" in sen[i] or "subscriber id, not valid" in sen[i]:
                temp = {}
                temp["command"] = "hangup" 
                temp["value"] = True
                temp['varified'] = False
                temp["comment"] = "not verified"
                response['action'].append(temp)

            elif "to access our company directory, please dial 9" in sen[i]:
                temp = {}
                temp["command"] = "DTMF" 
                temp["value"] = 9
                response['action'].append(temp)

            elif "dial the name feature, please dial 9" in sen[i]:
                temp = {}
                temp["command"] = "DTMF" 
                temp["value"] = 9
                response['action'].append(temp)
            
            elif "if you need to contact our company, please" in sen[i]:
                try:
                    if "press 5" in sen[i+1]:
                        temp = {}
                        temp["command"] = "DTMF" 
                        temp["value"] = 5
                        response['action'].append(temp)
                except:
                    pass
            
            elif "enter the last name of the person you are calling followed by the first name" in sen[i] and "when finished entering name" in sen[i]:
                temp = {}
                temp["command"] = "DTMF_string" 
                temp["value"] = f"{userdetails['lname']} {userdetails['fname']}#"
                response['action'].append(temp)
            
            elif "enter the first2 or more letters of the person's last name." in sen[i]:
                temp = {}
                temp["command"] = "DTMF_string" 
                temp["value"] = f"{userdetails['lname']}"
                response['action'].append(temp)
            
            elif "please leave your message after the tone. when done, hang up,or press the pound key." in sen[i] or "please leave your name, number, and message, and i'll textget back with you." in sen[i] or "angela elder i'm currently unavailable to take your call please leave a message" in sen[i] or "the name of the person you want to contact but i can't find it" in sen[i] or "but i can't find it" in sen[i]:
                temp = {}
                temp["command"] = "hangup" 
                temp["value"] = True
                temp['varified'] = False
                temp["comment"] = "not verified"
                response['action'].append(temp)
            
            elif "say yes or no" in sen[i-1] and "press 1" in sen[i]:
                temp = {}
                temp["command"] = "DTMF" 
                temp["value"] = 1
                response['action'].append(temp)
            
            elif "to enter the name of the person you're trying to reach" in sen[i]:
                try:
                    if "press 2" in sen[i+1]:
                        temp = {}
                        temp["command"] = "DTMF" 
                        temp["value"] = 2
                        response['action'].append(temp)
                except:
                    pass
            
            elif "no matching names. try a different spelling" in sen[i]:
                temp = {}
                temp["command"] = "hangup" 
                temp["value"] = True
                temp['varified'] = False
                temp["comment"] = "not verified"
                response['action'].append(temp)
            
            elif "select 3 to access our select by name directory" in sen[i] or "select 3 to access us hours select by name directory" in sen[i]:
                temp = {}
                temp["command"] = "DTMF"
                temp["value"] = 3
                response['action'].append(temp)
            
            elif "please enter the first few letters of the name of the person you would like to speak to" in sen[i]:
                temp = {}
                temp["command"] = "DTMF_string" 
                temp["value"] = f"{userdetails['fname']}"
                response['action'].append(temp)
            
            elif "to dial by name" in sen[i] and "press the pound sign" in sen[i]:
                temp = {}
                temp["command"] = "DTMF" 
                temp["value"] = "#"
                response['action'].append(temp)
            
            elif "please enter the first 3 letters of your party's first or last name" in sen[i]:
                temp = {}
                temp["command"] = "DTMF_string" 
                temp["value"] = f"{userdetails['fname'][:3]}"
                response['action'].append(temp)

            elif "for the company directory, please dial 1" in sen[i]:
                temp = {}
                temp["command"] = "DTMF" 
                temp["value"] = 1
                response['action'].append(temp)
            
            elif "you may also access our dial by name directory by pressing pound." in sen[i]:
                temp = {}
                temp["command"] = "DTMF" 
                temp["value"] = "#"
                response['action'].append(temp)
            
            elif "for a dial by name directory, please press the star key" in sen[i]:
                temp = {}
                temp["command"] = "DTMF" 
                temp["value"] = "*"
                response['action'].append(temp)

            elif "enter last name and pound key" in sen[i]:
                temp = {}
                temp["command"] = "DTMF_string"
                temp["value"] = f"{userdetails['lname']}#"
                response['action'].append(temp)
            
            elif "press up to 6 letters of the person's last name" in sen[i]:
                temp = {}
                temp["command"] = "DTMF_string"
                temp["value"] = f"{userdetails['lname'][:6]}"
                response['action'].append(temp)
            
            elif "to dial by employee name" in sen[i]:
                temp = {}
                temp["command"] = "DTMF"
                temp["value"] = 4
                response['action'].append(temp)
            
            elif "to access our company directory" in sen[i] and "press 1" in sen[i+1]:
                temp = {}
                temp["command"] = "DTMF"
                temp["value"] = 1
                response['action'].append(temp)
        
            elif "enter last name and pound sign" in sen[i]:
                temp = {}
                temp["command"] = "DTMF_string"
                temp["value"] = f"{userdetails['lname']}#"
                response['action'].append(temp)
            
            elif "dial name feature" in sen[i] and "please dial 9" in sen[i]:
                temp = {}
                temp["command"] = "DTMF"
                temp["value"] = 9
                response['action'].append(temp)
            
            elif "if you know the name of the person" in sen[i] and "but not the extension number" in sen[i] and "press 9" in sen[i+1]:
                temp = {}
                temp["command"] = "DTMF"
                temp["value"] = 9
                response['action'].append(temp)
            
            elif "please dial the last name and then press the pound key at any time during this message" in sen[i]:
                temp = {}
                temp["command"] = "DTMF"
                temp["value"] = f"{userdetails['lname']}#"
                response['action'].append(temp)
            
            elif "when you have finished" in sen[i] and "press the pound key" in sen[i]:
                temp = {}
                temp["command"] = "DTMF"
                temp["value"] = "#"
                response['action'].append(temp)
            
            elif "i could not find a similar name or menu option." in sen[i]:
                temp = {}
                temp["command"] = "hangup" 
                temp["value"] = True
                temp['varified'] = False
                temp["comment"] = "not verified"
                response['action'].append(temp)

            elif "is this the name" in sen[i]:
                if userdetails['fname'] not in sen[i] and userdetails['lname'] not in sen[i]:
                    temp = {}
                    temp["command"] = "hangup" 
                    temp["value"] = True
                    temp['varified'] = False
                    temp["comment"] = "not verified"
                    response['action'].append(temp)
            
            elif "for the company directory, please press the pound key" in sen[i]:
                temp = {}
                temp["command"] = "DTMF"
                temp["value"] = "#"
                response['action'].append(temp)
            
            elif "but i'm not finding a match for that name" in sen[i]:
                temp = {}
                temp["command"] = "hangup" 
                temp["value"] = True
                temp['varified'] = False
                temp["comment"] = "not verified"
                response['action'].append(temp)
            
            elif "please speak the name of the person you wish to call" in sen[i]:
                temp = {}
                temp["command"] = "play"
                temp["value"] = f"{userdetails['fname']} {userdetails['lname']}"
                response['action'].append(temp)
            
            elif "for a company directory" in sen[i] and "9" in sen[i-1]:
                temp = {}
                temp["command"] = "DTMF"
                temp["value"] = 9
                response['action'].append(temp)
            
            elif "spell" in sen[i] or "enter" in sen[i] or "know" in sen[i] or "press" in sen[i] or "dial" in sen[i]:
                print("*"*20)
                print("Line 171 condition : If spell, enter , know , press and dial found in sen[i]")
                print("***************************")
                if "last and first" in sen[i] or "last name and first" in sen[i] or "last name first name" in sen[i] or "last in first name" in sen[i] or "last name and then spell the first name" in sen[i] or "last name first" in sen[i]:
                    print("*"*20)
                    print("Line 173 condition : If last and first, last name and first, last name first name, last in first name, last name and then spell the first name, last name first  found in sen[i]")
                    print("********** 1 ************")
                    try:
                        print("condition in try block")
                        temp = {}
                        temp["command"] = "DTMF_string"
                        temp["value"] = f"{userdetails['lname']} {userdetails['fname']}#" if "pound" in sen[i+1] or "followed by number sign" in sen[i] else f"{userdetails['lname']} {userdetails['fname']}"
                        response['action'].append(temp)
                    except Exception as e:
                        print("condition in except block")
                        print(e)
                        temp = {}
                        temp["command"] = "DTMF_string"
                        temp["value"] = f"{userdetails['lname']} {userdetails['fname']}"
                        response['action'].append(temp)
                
                elif "i'm sorry i could not find any names" in sen[i] or "the name you have entered does not exist" in sen[i] or "no matches found" in sen[i] or "directory is empty" in sen[i] or " i'm sorry i could not find any name" in sen[i] or "recording press" in sen[i] or "please record your message" in sen[i] or "no directory entries match your search" in sen[i]:
                    print("*"*20)
                    print("Line 190 condition : if the person's name does not exist") 
                    temp = {}
                    temp["command"] = "hangup" 
                    temp["value"] = True
                    temp['varified'] = False
                    temp["comment"] = "not verified"
                    response['action'].append(temp)
                
                elif "for our dial by name" in sen[i] and "1" in sen[i-1]:
                    temp = {}
                    temp["command"] = "DTMF"
                    temp["value"] = 1
                    response['action'].append(temp)
                
                elif "enter the first few letters of the person's first or last name followedby pound." in sen[i]:
                    temp = {}
                    temp["command"] = "DTMF_string"
                    temp["value"] = f"{userdetails['lname']}#"
                    response['action'].append(temp)
                
                elif "please enter the first few letters of the person's first or last name followed by pound" in sen[i]:
                    temp = {}
                    temp["command"] = "DTMF_string"
                    temp["value"] = f"{userdetails['lname'][:3]}#"
                    response['action'].append(temp)
                
                elif "please enter at least the first 3 letters of the person's last name" in sen[i] or "please enter the first 3 letters of the person's last name" in sen[i] or "please enter the first few letters of the person's first or last name" in sen[i] or "please enter the first 3 letters of your party's last name" in sen[i] or "enter the first few letters of the party's last" in sen[i]:
                    print("*"*20)
                    print("Line 200 condition : Enter the 1st 3 letter and the last 3 letter of the person's last name") 
                    temp = {}
                    temp["command"] = "DTMF_string"
                    if len(sen)>1:
                        temp["value"] = f"{userdetails['lname'][:3]}#" if "pound" in sen[i+1] or "followed by number sign" in sen[i] else f"{userdetails['lname'][:3]}"
                    else:
                        temp["value"] = f"{userdetails['lname'][:3]}#" if "pound" in sen[i] or "followed by number sign" in sen[i] else f"{userdetails['lname'][:3]}"
                    response['action'].append(temp)
                elif "first 3 digits of the first name" in sen[i]:
                    print("*"*20)
                    print("Line 207 condition : Enter the 1st 3 letter of the person's first name")
                    print('sentence=========',i, sen)
                    temp = {}
                    temp["command"] = "DTMF_string"
                    if len(sen)>1:
                        temp["value"] = f"{userdetails['fname'][:3]}#" if "pound" in sen[i+1] or "followed by number sign" in sen[i] else f"{userdetails['fname'][:3]}"
                    else:
                        temp["value"] = f"{userdetails['fname'][:3]}#" if "pound" in sen[i] or "followed by number sign" in sen[i] else f"{userdetails['fname'][:3]}"
                    response['action'].append(temp)
                
                elif "please enter the first or last name of the party you wish to reach" in sen[i] and "press star" in sen[i+1]:
                    temp = {}
                    temp["command"] = "DTMF_string"
                    temp["value"] = f"{userdetails['lname']}"
                    response['action'].append(temp)

                elif "first 3 or more letters of the party's first or last name" in sen[i]:
                    temp = {}
                    temp["command"] = "DTMF_string"
                    temp["value"] = f"{userdetails['lname'][:3]}"
                    response['action'].append(temp)
                
                elif "first and last" in sen[i] or "first name and last" in sen[i] or "first or last" in sen[i]:
                    print("*"*20)
                    print("Line 208 condition : From first and last, first name and last, first or last in sen[i]")
                    # print("********** 2 ************")
                    try:
                        print("*"*20)
                        print("Line 205 condition : This is in Try block")
                        temp = {}
                        temp["command"] = "DTMF_string"
                        temp["value"] = f"{userdetails['fname']} {userdetails['lname']}#" if "pound" in sen[i+1] or "followed by number sign" in sen[i] else f"{userdetails['fname']} {userdetails['lname']}"
                        response['action'].append(temp)
                    except Exception as e:
                        print("*"*20)
                        print("Line 219 condition : This is in Except block")
                        print(e)
                        temp = {}
                        temp["command"] = "DTMF_string"
                        temp["value"] = f"{userdetails['fname']} {userdetails['lname']}"
                        response['action'].append(temp)
                
                elif "to dial by first name" in sen[i] and "press 1" in sen[i+1]:
                    temp = {}
                    temp["command"] = "DTMF"
                    temp["value"] = 1
                    response['action'].append(temp)
                
                elif "company directory by last name" in sen[i] and "press star" in sen[i+1]:
                    temp = {}
                    temp["command"] = "DTMF"
                    temp["value"] = "*"
                    response['action'].append(temp)
                
                elif "name not found. enter last name and pound key." in sen[i]:
                    temp = {}
                    temp["command"] = "hangup" 
                    temp["value"] = True
                    temp['varified'] = False
                    temp["comment"] = "not verified"
                    response['action'].append(temp)
                
                elif "first name" in sen[i]:
                    print("*"*20)
                    print("Line 227 condition : First name in sen[i]")
                    # print("********** 3 ************")
                    try:
                        print("*"*20)
                        print("Line 231 condition : In the try block")
                        temp = {}
                        temp["command"] = "DTMF_string"
                        temp["value"] = f"{userdetails['fname']}#" if "pound" in sen[i+1] or "followed by number sign" in sen[i] else f"{userdetails['fname']}"
                        response['action'].append(temp)
                    except Exception as e:
                        print("*"*20)
                        print("Line 238 condition : Except block")
                        print(e)
                        temp = {}
                        temp["command"] = "DTMF_string"
                        temp["value"] = f"{userdetails['fname']}#" if "pound" in sen[i] or "followed by number sign" in sen[i] else f"{userdetails['fname']}"
                        response['action'].append(temp)
                elif "last name" in sen[i] or "last name first" in sen[i]:
                    print("*"*20)
                    print("Line 246 condition : last name, last name first in sen[i]")
                    # print(f"_________Sentence[i+1] check :__________{sen[i+1]}___________________")
                    # print("********** 4 ************")
                    if "press the pound key and use the dialpad to spell the last name" in sen[i]:
                        temp = {}
                        temp["command"] = "DTMF_string"
                        temp["value"] = f"#{userdetails['lname']}"
                        response['action'].append(temp)
                    
                    elif "your party's last name please dial the last name and then press the pound key" in sen[i]:
                        temp = {}
                        temp["command"] = "DTMF_string"
                        temp["value"] = f"{userdetails['lname']}#"
                        response['action'].append(temp)
                    
                    elif "last name and" in sen[i] and "pound" in sen[i+1]:
                        print("*"*20)
                        print("Line 250 condition : last name and, pound in sen[i+1]")
                        temp = {}
                        temp["command"] = "DTMF_string"
                        temp["value"] = f"{userdetails['lname']}#"
                        response['action'].append(temp)
                    
                    elif "spell the 1st and last name then" in sen[i] and "pound" in sen[i+1]:
                        temp = {}
                        temp["command"] = "DTMF_string"
                        temp["value"] = f"{userdetails['fname']} {userdetails['lname']}#"
                        response['action'].append(temp)
                    
                    elif "spell the last name of the person" in sen[i] and "pound" in sen[i+1]:
                        temp = {}
                        temp["command"] = "DTMF_string"
                        temp["value"] = f"{userdetails['lname']}#"
                        response['action'].append(temp)
                    
                    elif "enter the first three letters of the person's last name" in sen[i]:
                        temp = {}
                        temp["command"] = "DTMF_string"
                        temp["value"] = f"{userdetails['lname'][:3]}"
                        response['action'].append(temp)
                    
                    elif "into the first few letters of the party's last name" in sen[i]:
                        temp = {}
                        temp["command"] = "DTMF_string"
                        temp["value"] = f"{userdetails['lname']}"
                        response['action'].append(temp)
                    
                    elif "if you know your party's last name, please dial the last name.and then press the pound key" in sen[i]:
                        temp = {}
                        temp["command"] = "DTMF_string"
                        temp["value"] = f"{userdetails['lname']}#"
                        response['action'].append(temp)
                    
                    elif "to dial by last name" in sen[i] and "pound" in sen[i-1]:
                        temp = {}
                        temp["command"] = "DTMF"
                        temp["value"] = "#"
                        response['action'].append(temp)
                    
                    elif "please enter last name of the person you wish to speak to" in sen[i]:
                        temp = {}
                        temp["command"] = "DTMF_string"
                        temp["value"] = f"{userdetails['lname']}"
                        response['action'].append(temp)
                    
                    elif "enter the first 2 or more letters of the person's last name" in sen[i]:
                        temp = {}
                        temp["command"] = "DTMF_string"
                        temp["value"] = f"{userdetails['lname']}"
                        response['action'].append(temp)
                    
                    else:
                        print("*"*20)
                        print("Line 257 condition : if not found last name and, pound in sen[i+1]")
                        value = getno.findall(sen[i+1]) if i+1 <= len(sen) else None 
                        if value and "at least" not in sen[i]:
                            print("*"*20)
                            print("Line 261 condition : if value and 'at least' not in sen[i]")
                            temp = {}
                            temp["command"] = "DTMF" 
                            temp["value"] = strtoint.get(value[0])
                            response['action'].append(temp)
                        else:
                            print("*"*20)
                            print("Line 268 condition : if value and 'at least' in sen[i]")
                            try:
                                print("*"*20)
                                print("Line 264 condition : In the try block")
                                temp = {}
                                temp["command"] = "DTMF_string"
                                temp["value"] = f"{userdetails['lname']}#" if "pound" in sen[i+1] or "followed by number sign" in sen[i] else f"{userdetails['lname']}"
                                response['action'].append(temp)
                            except Exception as e:
                                print("*"*20)
                                print("Line 278 condition : In the except block")
                                print(e)
                                temp = {}
                                temp["command"] = "DTMF_string"
                                temp["value"] = f"{userdetails['lname']}"
                                response['action'].append(temp)
                elif "employee listing" in sen[i]:
                    print("*"*20)
                    print("Line 299 condition : if employee listing in found in senentence")
                    value = getno.findall(sen[i - 1])
                    words = sen[i - 1].split()
                    value_dist = [
                        abs(words.index("listing") - words.index(v)) for v in value
                    ]

                    value = [value[value_dist.index(min(value_dist))]]
                
                elif "if you would like our dial by name directory please" in sen[i]:
                    value = getno.findall(sen[i+1])
                    temp = {}
                    temp["command"] = "DTMF"
                    temp["value"] = int(value[0])
                    response['action'].append(temp)
                
                elif "dial by name directory please press the star key" in sen[i] or "except by both email and phone for dial by name directory" in sen[i]:
                    temp = {}
                    temp["command"] = "DTMF"
                    temp["value"] = "*"
                    response['action'].append(temp)
                
                elif "there are no matches to the 3 letters" in sen[i]:
                    temp = {}
                    temp["command"] = "hangup" 
                    temp["value"] = True
                    temp['varified'] = False
                    temp["comment"] = "not verified"
                    response['action'].append(temp)
                
                elif "for staff directory, please dial 9" in sen[i]:
                    temp = {}
                    temp["command"] = "DTMF"
                    temp["value"] = 9
                    response['action'].append(temp)
                
                elif "for the company directory, dial 8 to be connected to the operator" in sen[i]:
                    temp = {}
                    temp["command"] = "DTMF"
                    temp["value"] = 8
                    response['action'].append(temp)
                
                elif "if you would like our dial by name directory" in sen[i] and "press 1" in sen[i+1]:
                    temp = {}
                    temp["command"] = "DTMF" 
                    temp["value"] = 1
                    response['action'].append(temp)
                
                elif "to use our dial by name" in sen[i] and "1" in sen[i-1] and "company directory" in sen[i]:
                    temp = {}
                    temp["command"] = "DTMF" 
                    temp["value"] = 1
                    response['action'].append(temp)
                
                elif "for our company staff directory" in sen[i] and "press 1" in sen[i+1]:
                    temp = {}
                    temp["command"] = "DTMF"
                    temp["value"] = 1
                    response['action'].append(temp)
                
                elif "if you know your party's extension, you may enter it now or press the pound key to access the company directory." in sen[i]:
                    temp = {}
                    temp["command"] = "DTMF"
                    temp["value"] = "#"
                    response['action'].append(temp)
                
                elif "directory" in sen[i]:
                    print("*"*20)
                    print("Line 287 condition : if directroy in found in sen[i]")
                    print("********DIRECTORY**************")
                    if "staff directory" in sen[i] or "to consult our directory" in sen[i] or "to access our company directory" in sen[i] or  "to the local at 17 directory" in sen[i] or "name directory" in sen[i]:
                        print("*"*20)
                        print("Line 291 condition : to access our staff directory, to consult our directory, dial by name directory, to access our company directory, to the local at 17 directory in sen[i]")
                        value = getno.findall(sen[i - 1])
                        print("value=====================",value)
                        print("sentence===============",sen[i])
                        print("I===========================",i)
                        words = sen[i - 1].split()
                        print("words=================", words)
                        try :
                            value_dist = [
                                abs(words.index("directory") - words.index(v)) for v in value
                            ]

                            value = [value[value_dist.index(min(value_dist))]]
                        except ValueError as ve:
                            print("**********Run valuerror cell***********")
                            pass 
                    
                    elif "dial 4 for the company directory" in sen[i]:
                        print("*"*20)
                        print("Line 295 condition : if dial 4 for the company directory in sen[i]")
                        temp["command"] = "DTMF"
                        temp["value"] = 4
                        response['action'].append(temp)
                    elif "company directory please dial 2" in sen[i]:
                        print("*"*20)
                        print("Line 301 condition : company directory please dial 2 in sen[i]")
                        temp["command"] = "DTMF"
                        temp["value"] = 2
                        response['action'].append(temp)                        

                    elif "to access our company directory please dial 2" in sen[i]:
                        print("*"*20)
                        print("Line 308 condition : to access our company directory please dial 2 in sen[i]")
                        temp["command"] = "DTMF"
                        temp["value"] = 2
                        response['action'].append(temp)

                    elif "to the local at 17 directory" in sen[i]:
                        print("*"*20)
                        print("Line 315 condition : to the local at 17 directory in sen[i]")
                        temp["command"] = "DTMF"
                        temp["value"] = "#"
                        response['action'].append(temp)

                    elif "you may dial pound for the company directory for customer service" in sen[i]:
                        print("*"*20)
                        print("Line 322 condition : you may dial pound for the company directory for customer service in sen[i]")
                        temp["command"] = "DTMF"
                        temp["value"] = "#"
                        response['action'].append(temp)
                    
                    elif "please dial it now to access the company directory press the pound key followed by number one" in sen[i]:
                        print("*"*20)
                        temp["command"] = "DTMF_String"
                        temp["value"] = "#1"
                        response['action'].append(temp)
                    
                    elif "to be directed to customer support please" in sen[i]:
                        print("*"*20)
                        print("Line 336 condition : to be directed to customer support please in sen[i]")
                        temp["command"] = "DTMF"
                        temp["value"] = 1
                        response['action'].append(temp)
                    
                    elif "for a dial by name" in sen[i] and "8" in sen[i-1]:
                        temp["command"] = "DTMF"
                        temp["value"] = 8
                        response['action'].append(temp)
                    
                    elif "for a company directory, press the star key." in sen[i]:
                        temp = {}
                        temp["command"] = "DTMF"
                        temp["value"] = "*"
                        response['action'].append(temp)
                    
                    else:
                        print("*"*20)
                        print("Line 343 condition : If all directory condition false then do this")
                        value = getno.findall(sen[i+1]) if i+1 <= len(sen) else None
                    if value:
                        print("*"*20)
                        print('&&&& SENTECE &&&&&&&',sen[i])
                        print("Line 347 condition : if value is exist")
                        temp["command"] = "DTMF"
                        temp["value"] = strtoint.get(value[0])
                        response['action'].append(temp)
                    elif "name" in sen[i]:
                        print("*"*20)
                        print("Line 353 condition : if name in sen[i]")
                        value = getno.findall(sen[i+1]) if i+1 <= len(sen) else None 
                        if value:
                            temp = {}
                            temp["command"] = "DTMF" 
                            temp["value"] = strtoint.get(value[0])
                            response['action'].append(temp)
                
                elif "dial by name" in sen[i]:
                    value = getno.findall(sen[i+1]) if i+1 <= len(sen) else None
                    temp["command"] = "DTMF" 
                    temp["value"] = strtoint.get(value[0])
                    response['action'].append(temp)
                
                elif "voice messaging service" in sen[i] or "please call back the next business day" in sen[i] or "you want to reach you may dial it now" in sen[i]:
                    print("Line 401 condition: To hangup after receiving 'press' word.")
                    temp = {}
                    temp["command"] = "hangup" 
                    temp["value"] = True
                    temp['varified'] = False
                    temp["comment"] = "not verified"
                    response['action'].append(temp)
            elif "employee listing" in sen[i]:
                print("*"*20)
                print("Line 405 condition : if employee listing in found in senentence")
                value = getno.findall(sen[i - 1])
                words = sen[i - 1].split()
                value_dist = [
                    abs(words.index("listing") - words.index(v)) for v in value
                ]

                value = [value[value_dist.index(min(value_dist))]]
            
            elif "you need to contact our company please" in sen[i]:
                value = getno.findall(sen[i + 1])
                temp["value"] = int(value[0])
                temp["comment"] = "DTMF"
                response['action'].append(temp)
            
            elif "if you would like to search the directory by name." in sen[i] and "2" in sen[i-1]:
                temp = {}
                temp["command"] = "DTMF"
                temp["value"] = 2
                response['action'].append(temp)
            
            elif "directory" in sen[i]:
                print("*"*20)
                print("Line 362 condition : if directory in sen[i]")
                if "to access our staff directory" in sen[i] or "to consult our directory" in sen[i] or "to access our company directory" in sen[i] or  "to the local at 17 directory" in sen[i] or  "for the directory for operator assistance" in sen[i] or "name directory" in sen[i]:
                    print("*"*20)
                    print("Line 365 condition : to access our staff directory, to consult our directory, to access our company directory, to the local at 17 directory, for the directory for operator assistance in sen[i]")
                    value = getno.findall(sen[i-1])
                elif "dial 4 for the company directory" in sen[i]:
                    print("*"*20)
                    print("Line 369 condition : if dial 4 for the company directory in sen[i]")
                    temp["command"] = "DTMF"
                    temp["value"] = 4
                    response['action'].append(temp)
                
                elif "for our company directory." in sen[i] and "1" in sen[i-1]:
                    temp = {}
                    temp["command"] = "DTMF"
                    temp["value"] = 1
                    response['action'].append(temp)
                
                elif "for a company directory by name" in sen[i] and "7" in sen[i-1]:
                    temp = {}
                    temp["command"] = "DTMF"
                    temp["value"] = 7
                    response['action'].append(temp)
                    
                else:
                    print("*"*20)
                    print("Line 375 condition : else do this")
                    value = getno.findall(sen[i+1]) if i+1 <= len(sen) else None
                if value:
                    print("*"*20)
                    print("Line 379 condition : if value is exist")
                    temp["command"] = "DTMF"
                    temp["value"] = strtoint.get(value[0])
                    response['action'].append(temp)
                elif "name" in sen[i]:
                    print("*"*20)
                    print("Line 385 condition : if dial 4 for the company directory in sen[i]")
                    value = getno.findall(sen[i+1]) if i+1 <= len(sen) else None 
                    if value:
                        temp = {}
                        temp["command"] = "DTMF" 
                        temp["value"] = strtoint.get(value[0])
                        response['action'].append(temp)
            
            elif "type the last name followed by the first name of the person you're trying to reach." in sen[i]:
                temp = {}
                temp["command"] = "DTMF_string"
                temp["value"] = f"{userdetails['fname']} {userdetails['lname']}"
                response['action'].append(temp)
            
            elif "you like to reach" in sen[i]:
                print("*"*20)
                print("Line 395 condition : if you like to reach in sen[i]")
                temp = {}
                temp["command"] = "play"
                temp["value"] = f"{userdetails['fname']} {userdetails['lname']}"
                response['action'].append(temp)
            elif "dial by name" in sen[i] or "dial by last name" in sen[i]:
                print("*"*20)
                print("Line 402 condition : dial by name, dial by last name in sen[i]")
                if "to dial by" in sen[i]:
                    value = getno.findall(sen[i-1])
                else:
                    value = getno.findall(sen[i+1]) if i+1 <= len(sen) else None if i+1 < len(sen) else getno.findall(sen[i-1])
                if value:
                    temp = {}
                    temp["command"] = "DTMF" 
                    temp["value"] = strtoint.get(value[0])
                    response['action'].append(temp)
            elif "last name" in sen[i]:
                print("*"*20)
                print("Line 414 condition : last name in sen[i]")
                value = getno.findall(sen[i+1]) if i+1 <= len(sen) else None 
                if value:
                    temp = {}
                    temp["command"] = "DTMF" 
                    temp["value"] = strtoint.get(value[0])
                    response['action'].append(temp)
            elif "hear the next name" in sen[i]:
                print("*"*20)
                print("Line 423 condition : hear the next name in sen[i]")
                value = getno.findall(sen[i+1]) if i+1 <= len(sen) else None 
                if value:
                    temp = {}
                    temp["command"] = "DTMF" 
                    temp["value"] = strtoint.get(value[0])
                    # response['action'].append(temp)
            elif "not finding a match for that name" in sen[i] or "no matching names" in sen[i]:
                print("*"*20)
                print("Line 432 condition : not finding a match for that name, no matching names in sen[i]")
                temp = {}
                temp["command"] = "hangup" 
                temp["value"] = True
                temp['varified'] = False
                temp["comment"] = "name not recognised"
                response['action'].append(temp)

            elif "by security. for message at the tone. when you are finished, hang up" in sen[i]:
                pass
            
            elif (len(response['action'])>=1) and "now to leave a message in our general mailbox please" in sen[i] or "if you would like to leave a message" in sen[i] or "to leave a message in our general mail" in sen[i]:
                pass
            
            elif "please call back during our normal business hours" in sen[i] or "please leave your message" in sen[i] or "you've reached the voicemail" in sen[i] or "hi you've reached" in sen[i] or "I'm sorry I could not find any names that match your entry" in sen[i] or "will return your call as soon as possible thank you" in sen[i] or "to leave a voicemail" in sen[i] or "i connect your call" in sen[i] or "nothing service at this time" in sen[i] or "waiting please stand bye" in sen[i] or "will get back to you shortly" in sen[i] or "please leave us your name" in sen[i] or "we will return your call as soon as possible" in sen[i] or "i'll call you back" in sen[i] or "hello testing repertory" in sen[i] or "four easy links product support" in sen[i] or "hang up" in sen[i] or "i'll get back to you" in sen[i] or "voice messages" in sen[i] or "voicemail" in sen[i] or "leave a message" in sen[i] or "automated voice" in sen[i] or "recording press" in sen[i] or "automatic voice message" in sen[i] or "please record your message" in sen[i] or "please leave a message after the tone" in sen[i] or "sorry.there are no more names that match your entry. goodbye." in sen[i]:
                print("*"*20)
                print("Line 442 condition : please call back during our normal business hours, please leave your message, you've reached the voicemail, hi you've reached in sen[i]")
                print("((((((( Sentence )))))))))))", sen[i])
                # print("^^^^^^^ Temp value ^^^^^^^^^  ", temp)
                # print("^^^^^^^ Response ^^^^^^^^^  ",response['action'])

                if len(response['action'])==0:
                    temp = {}
                    temp["command"] = "hangup" 
                    temp["value"] = True
                    temp['varified'] = False
                    temp["comment"] = "not verified"
                    response['action'].append(temp)
                else:
                    pass

            elif "transferring your call to michael burns." in sen[i]:
                temp = {}
                temp['command'] = "hangup"
                temp['value'] = True
                temp['partial_verify'] = True
                response['action'].append(temp)
            
            elif "just tell me their name" in sen[i]:
                temp["command"] = "play"
                temp["value"] = f"{userdetails['fname']} {userdetails['lname']}"
                response['action'].append(temp)
            
            elif "who would you like to reach" in sen[i] and "say" in sen[i]:
                temp = {}
                temp["command"] = "play"
                temp["value"] = f"{userdetails['fname']} {userdetails['lname']}"
                response['action'].append(temp)
            
            # elif "directory" not in sen[i]:
            #     print(f"This is sen[i]______________{sen[i]}")
            #     temp = {}
            #     temp["command"] = "hangup" 
            #     temp["value"] = True
            #     temp['varified'] = False
            #     temp["comment"] = "not verified"
            #     response['action'].append(temp)
        
    except Exception as e:
        print(e)
    finally : 
        print(response)
        return jsonify(response)
