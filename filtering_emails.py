# Amanda Foun
# 6-3 GOAL: sort through the json files and make it more readable
# 6-4 GOAL: use regular expressions to clean up to/from fields
#           group data based on To, From, Date   
# 6-5 GOAL: add PERIOD LABELS + PERSON LABELS (later, content labels) keys to the dictionary  

import json
import base64
import re # allows us to use regular expressions to clean up email addresses
import datetime
import time
from collections import Counter

pplDict = {'Faculty': ['rpricejo@wellesley.edu', 'fturbak@wellesley.edu', 'slee@wellesley.edu', 'sbuck@wellesley.edu'], 
            'StudentLdr': ['jcherayi@wellesley.edu', 'mfendroc@wellesley.edu', 'afoun@wellesley.edu', 'mjain2@wellesley.edu', 'mjung@wellesley.edu', 'ctsui@wellesley.edu', 'svoigt@wellesley.edu', 'sburns@wellesley.edu', 'bcarver@wellesley.edu'],
            'Admin': ['rpurcell@wellesley.edu'],
            'GoogleGroup': ['cs111-spring15@wellesley.edu']}

def getEmailAddress(addressLine):
    '''helper function for sort() that uses regular expressions'''
    '''returns a list of the email address(es) in the form xxx@wellesley.edu'''
    match = re.findall(r'[\w\.-]+@[\w\.-]+', addressLine) # finds the email address 
    return match
    
def getMonth(month_str):
    '''helper function for getTime()'''
    '''returns the number associated with the given month'''
    if month_str == 'Jan':
        return int(1)
    elif month_str == 'Feb':
        return int(2)
    elif month_str == 'Mar':
        return int(3)
    elif month_str == 'Apr':
        return int(4)
    elif month_str == 'May':
        return int(5)
    elif month_str == 'Jun':
        return int(6)

# args timestamp will be in the form (string)
# Sun, 1 Feb 2015 06:33:04 -0800 (PST)
# Sat, 31 Jan 2015 19:45:51 -0800 (PST)
               
def getDate(timestamp): 
    '''helper funtion for sort() that uses datetime module'''
    '''returns the date in the form yyyy-mm-dd'''
    timeInfo = timestamp.split() # divides the timestamp values (strings) into a list
    yr = int(timeInfo[3])
    month = getMonth(timeInfo[2])
    day = int(timeInfo[1])
    time = datetime.date(yr,month,day)
    return time.isoformat() # this makes it return in the readable format

def getTime(timestamp): 
    '''helper funtion for sort() that uses datetime module'''
    '''returns the time in the form hh:mm:ss'''
    timeInfo = timestamp.split() # divides the timestamp values (strings) into a list
    hms_string = timeInfo[4].split(':') # splits the time data into a list [h,m,s]
    hms = map(int,hms_string) # converts all hr, min, sec values to integers
    h = hms[0]
    m = hms[1]
    s = hms[2]
    time = datetime.time(h,m,s)
    return time.isoformat() # this makes it return in the readable format

def addPeriodLabel(time):
    '''@time: time email was sent'''
    '''returns a list of period labels'''
    #if addPeriodLacel
    pass                                  

def addToPersonLabel(toEmail):
    '''@to: email was sent to this email address (list of str)'''
    '''returns a list of person labels'''
    for k in pplDict.keys():
        for e in toEmail: 
            if e in pplDict.get(k): # if email address is a faculty's, student leader's or admin's
                return k
    return 'Student' # not faculty, studentldr or administration so assuming it's a student   

def addFromPersonLabel(fromEmail):
    '''@from: email was sent from this email address (list of str)'''
    '''returns a list of person labels'''
    for k in pplDict.keys(): 
        for e in fromEmail:
            if e in pplDict.get(k): # if email address is a faculty's, student leader's or admin's
                return k
    return 'Student'  # not faculty, studentldr or administration so assuming it's a student                                                                                                                                                                                                                                                                                                                                                                                                                                                   
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
def sort(emails): # when testing, use message
    '''Returns a list of dictionaries, where each elt of the list 
    is a separate email. KEYS: to, from, time, body, threadID'''
    emailList = [] # will store each dictionary
    
    for i in range(len(emails)): # loop through each email in the message list
        emailDict = {}   
        messageList = [] # will contain the body of the email
        
        # this ensures that we can get the body of each email
        try:
            msg_str = base64.urlsafe_b64decode(emails[i]['payload']['parts'][0]['parts'][0]['body']['data'].encode('ASCII'))
        except KeyError:
            try:
                msg_str = base64.urlsafe_b64decode(emails[i]['payload']['parts'][0]['body']['data'].encode('ASCII'))
            except KeyError:
                try:
                    msg_str = base64.urlsafe_b64decode(emails[i]['payload']['body']['data'].encode('ASCII'))
                except KeyError:
                    pass
                   
        for line in msg_str.split('\r'):
            if 'On Mon' in line or 'On Tue' in line or 'On Wed' in line or 'On Thu' in line or 'On Fri' in line or 'On Sat' in line or 'On Sun' in line or 'You received this message because you are subscribed to the Google Groups ' in line or 'Best,' in line or 'Regards,' in line or 'Thanks' in line:
                break
            if line != '\n':
                messageList.extend(line.split('\n'))
            for item in messageList:
                if item == '':
                    messageList.remove(item)
        
        emailDict['BODY'] = ' '.join(messageList)
        emailDict['THREADID'] = emails[i]['threadId']
        emailDict['TIME'] = emails[i]['payload']['headers'][1]['value'].split(';')[1].strip('   ')
        timestamp = emails[i]['payload']['headers'][1]['value'].split(';')[1].strip('   ')
        #print getTime(timestamp)[:10]
        emailDict['DATE'] = getDate(timestamp)
        emailDict['TIME'] = getTime(timestamp)
        

        # at each index j, there is a dictionary
        for j in range(len(emails[i]['payload']['headers'])):
            if emails[i]['payload']['headers'][j].values()[0] == 'Subject':
                emailDict['SUBJECT'] = emails[i]['payload']['headers'][j].values()[1]
            if emails[i]['payload']['headers'][j].values()[0] == 'To':
                toAddress = emails[i]['payload']['headers'][j].values()[1]
                email = getEmailAddress(toAddress)
                emailDict['TO'] = email #adds just the email address, not the name to the dictionary
                emailDict['TO_LABEL'] = addToPersonLabel(email)
            if emails[i]['payload']['headers'][j].values()[0] == 'From':
                fromAddress =emails[i]['payload']['headers'][j].values()[1]
                email2 = getEmailAddress(fromAddress)
                emailDict['FROM'] = email2
                emailDict['FROM_LABEL'] = addFromPersonLabel(email2)
        emailList.append(emailDict)
    return emailList     

def printList(inputList):
    '''prints out each element of the list on a new line'''
    for i in range(len(inputList)):
        print inputList[i]
        print '\n'

def countTo(listOfDictionaries):
    '''returns a list of dictionaries, key=email and value=# of emails sent to that user'''
    '''takes in a list of dictionaries that contain all info about the emails'''
    allAddresses = [] # list of all the addresses that received emails 
    toList = [] # list of dictionaries
    for dct in listOfDictionaries: # loop through all the dictionaries
        allAddresses.append(dct['TO']) # dct['TO'] are the email addresses
    for a in range(len(allAddresses)): # loop through all addresses
        toDict = {} # key=email address, value =# of emails sent to that address 
        num = allAddresses.count(allAddresses[a]) # number mssgs sent to that email 
        #for d in toList:
        #    if ", ".join(allAddresses[a]) in d.keys():
        toDict[", ".join(allAddresses[a])]=num
        if toDict not in toList:
            toList.append(toDict)
    return toList

def countFrom(listOfDictionaries):
    '''returns a list of dictionaries, key=email and value=# of emails that user sent'''
    '''@listOfDictionaries: list of dictionaries that contain all info about the emails'''
    allAddresses = [] # list of all the addresses that sent emails 
    fromList = [] # list of dictionaries
    for dct in listOfDictionaries: # loop through all the dictionaries
        allAddresses.append(dct['FROM']) # dct['FROM'] are the email addresses
    for a in range(len(allAddresses)): # loop through all addresses
        fromDict = {} # key=email address, value =# of emails sent to that address 
        num = allAddresses.count(allAddresses[a]) # number mssgs sent to that email 
        fromDict[", ".join(allAddresses[a])]=num
        if fromDict not in fromList:
            fromList.append(fromDict)
    return fromList

def countDays(listOfDictionaries):
    '''returns a list of dictionaries, key=date and value=# of emails sent that day'''
    '''@listOfDictionaries: list of dictionaries that contain all info about the emails'''
    allDays = []
    countList = []
    for dct in listOfDictionaries: # loop through all the dictionaries
        allDays.append(dct['DATE']) # add the timestamps to the list
    for t in range(len(allDays)):
        daysDict = {}
        num = allDays.count(allDays[t])
        daysDict[allDays[t]]=num
        if daysDict not in countList:
            countList.append(daysDict)
    return countList
        

def countOneDay(listOfDictionaries,date):
    '''returns a list of dictionaries, key=hour and value=# of emails sent that hour'''
    '''@listOfDictionaries: list of dictionaries that contain all info about the emails'''
    '''@date: in the form (string) yyyy-mm-dd'''
    allTimes = []
    countList = []
    for dct in listOfDictionaries: # loop through all the dictionaries
        if dct['DATE']==date:
            allTimes.append(dct['TIME'][1]) # add the timestamps to the list
    for t in range(len(allTimes)):
        dayDict = {}
        num = allTimes.count(allTimes[t])
        dayDict[allTimes[t]+":00"]=num
        if dayDict not in countList:
            countList.append(dayDict) 
    return countList        
     

# ~~TESTING 

# reads the json file and prints it out
json_data = open("cs111EmailsALL.json").read()
message = json.loads(json_data) # format=full  
listOfEmails = sort(message)
#print listOfEmails
#print countTo(listOfEmails)
#print countFrom(listOfEmails)
#print countDays(listOfEmails)
#print countOneDay(listOfEmails,'2015-01-26')
printList(listOfEmails)
