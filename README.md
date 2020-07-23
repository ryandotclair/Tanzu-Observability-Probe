# WavefrontCodeStreamProbe
A simple Wavefront Probe written for a CodeStream pipeline (CI task), that checks if an alert was triggered. This is useful for CodeStream instances that sit behind a firewall (pull mechanism).

# Requirements / Assumptions
This script requires the `requests` library (`pip3 install requests`), and the assumption is you've added this to your Workspace container image (along with getting requests library installed). 

Assuming you've added this script to `/app/wave-probe.py`, you can get it working with the following steps:
```
export WFAUTH=${input.WAVEFRONT_TOKEN}
export WFPEVENTID=${input.WAVEFRONT_ALERT_ID}
export WFPBASEURL=surf.wavefront.com
python3 /app/wave-probe.py
export WAVE_STATUS=$(cat /app/set.txt)
```
> Note: this assumes you have `WAVEFRONT_TOKEN` and `WAVEFRONT_ALERT_ID` Inputs set in Code Stream. The Alert ID can be found in the URL of the Alert 
you wish to check. Replace `surf.wavefront.com` with your own wavefront instance (don't include any \'s).

You'll need to include `WAVE_STATUS` as one of the Exports in the CI task. Value of WAVE_STATUS will be one of three values: INIT (which means something went wrong with the script), NORMAL (Alert didn't fire in the default 5 min it monitors), or FIRING (alert triggered).

# Output
The preceeding CodeStream tasks can then check the value of WAVE_STATUS for FIRING (aka alert was triggered). Otherwise it will say "NORMAL" after 5 minutes (tunable by changing loop count and/or sleep count in the script)

Example of a CodeStream task's "Condition": 
```
$(Validate.Wavefront Probe.output.exports.WAVE_STATUS} == "FIRING"
```
> Note: it follows the StageName.TaskName.output.exports.ExportsName format.
