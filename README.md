# Overview
A simple Probe written for a Code Stream pipeline (SSH task), that checks if an alert was triggered. This is useful for Code Stream instances that sit behind a firewall (pull mechanism).

# Requirements / Assumptions
This script assumes you have the following environment variables set:
- `TO_TOKEN` (for your Tanzu Observability API token)
- `TO_EVENTID` (the unique alert ID that you're probing for... this is found in wavefront UI by selecting the alert in question and grabbing the # after "../alerts/#")
- `TO_BASEURL` (ex: surf.wavefront.com ... do not include "/")
- `SCRIPT_RESPONSE_FILE` (this is generated by Code Stream at task execution, and is how the response of the script is shared to other Code Stream tasks)

This also assumes the script is ran in a Code Stream ssh task, which requires you to run the following commands _before_ you execute this python script:
```
export TO_TOKEN=[API TOKEN]
export TO_EVENTID=[ALERT'S ID]
export TO_BASEURL=$ [x.wavefront.com]
export RESPONSE=$SCRIPT_RESPONSE_FILE
```

# Output
The preceeding Code Stream tasks can then check the response file for the SSH task that this script is ran in for FIRING (aka alert was triggered). Otherwise it will say "NORMAL" after 5 minutes (tunable by changing loop count and/or sleep count)

Example of a Code Stream task's "Condition": `$(Push to Prod.TO Probe.output.response} == "FIRING"`
