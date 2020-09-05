#! /bin/python3
import os
import time
import requests
import logging

# DEPENDENCIES:
# This assumes you have the following environment variables set:
#   - TO_TOKEN (for your Wavefront API token)
#   - TO_EVENTID (the unique alert ID that you're probing for... this is found in wavefront UI by selecting the 
# alert in question and grabbing the number after "../alerts/#")
#   - TO_BASEURL (ex: surf.wavefront.com ... do not include "/")
#   - SCRIPT_RESPONSE_FILE (this is created by CodeStream)
#
# This also assumes the script is ran in a CodeStream ssh task, which requires you to run the following commands 
# _before_ you execute this python script:
#
# export TO_TOKEN=[API TOKEN]
# export TO_EVENTID=[ALERT'S ID]
# export TO_BASEURL=$ [x.wavefront.com]
# export RESPONSE=$SCRIPT_RESPONSE_FILE
#
# The preceeding CodeStream tasks can then check the response file for FIRING (alert was triggered). 
# Otherwise after it will say "NORMAL" after 4 minutes (tunable by changing loop count and/or sleep count)

#ENV VARs
TOAuth = "Bearer " + str(os.environ['TO_TOKEN']) #your Wavefront API token
eventID = os.environ['TO_EVENTID'] # unique alert ID that we're probing for
baseURL = os.environ['TO_BASEURL'] # example: surf.wavefront.com

#CONFIG
counter = 1
cmd = 'echo FIRING > $RESPONSE'
normal_cmd = 'echo NORMAL > $RESPONSE'
url = "https://" + baseURL + "/api/v2/alert/" + str(eventID)
head = {
    'Accept':'application/json',
    'Authorization': TOAuth
}

# Check first 5min of deployment if there's an issue
while counter < 60:
    counter += 1
    #Check Wavefront Alert's status
    r = requests.get(url, headers=head)
    rj = r.json()
    status=rj["response"]["status"][0]
    print ("status is: " + str(status))
    #If the alert is firing, it means there's an issue
    if "FIRING" in status:
        #Pass on to the response file that, which feeds into next
        #CodeStream task that there's an issue
        os.system(cmd)
        counter = 60
    elif counter == 59:
        os.system(normal_cmd)
        counter = 60
    else:
    #If therer's no issue, sleep for 5 seconds and try again
        print ("Going to sleep for 5 seconds")
        time.sleep(5)
        print ("Waking up")
