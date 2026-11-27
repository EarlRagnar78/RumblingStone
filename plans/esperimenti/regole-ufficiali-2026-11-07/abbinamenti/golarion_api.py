import json,subprocess,urllib.parse,sys
def q(**params):
    u='https://golarion.altervista.org/api.php?'+urllib.parse.urlencode({**params,'format':'json'})
    return json.loads(subprocess.run(['curl','-sS',u],capture_output=True,text=True).stdout)
