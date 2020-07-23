#! /bin/python3
import os
import time
import requests
import logging
import subprocess

#ENV VARs
wvAuth = "Bearer " + str(os.environ['WFAUTH'])
eventID = os.environ['WFPEVENTID']
baseURL = os.environ['WFPBASEURL'] # example: surf.wavefront.com

#CONFIG
counter = 0
os.environ['WAVE_STATUS'] = 'INIT'
url = "https://" + str(baseURL) + "/api/v2/alert/" + str(eventID)
head = {
    'Accept':'application/json',
    'Authorization': wvAuth
}

# Check first 10min of deployment if there's an issue
while counter < 60:
    counter += 1
    #Check Wavefront Alert's status
    r = requests.get(url, headers=head)
    rj = r.json()
    print (rj)
    status=rj["response"]["status"][0]
    print ("status is: " + str(status))
    #If the alert is firing, it means there's an issue
    if "FIRING" in status:
        #Set env var for the next CodeStream task to catch
        os.system("echo 'FIRING' > /app/set.txt")
        counter = 60
    elif counter == 59:
        #Set env var for the next CodeStream task to catch
        os.system("echo 'NORMAL' > /app/set.txt")
        print ("Alert never fired, setting env var WAVE_STATUS to NORMAL")
        counter == 60
    else:
    #If therer's no issue, sleep for 10 seconds and try again
        print ("Going to sleep for 10 seconds")
        time.sleep(5)
        print ("Waking up")
