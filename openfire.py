import shodan
import sys
import requests, time
from discord_webhook import DiscordWebhook
requests.packages.urllib3.disable_warnings() 

def discordMessage(text):
        webhook = DiscordWebhook(url=URLHERE, content=text)
        webhook.execute()



# Configuration
API_KEY = "W5aeOynZRxJG2TO1AGPykKY5sqZPjcIv"



# Input validation
if len(sys.argv) == 1:
        print('Usage: %s <text file of targets>' % sys.argv[0])
        sys.exit(1)

try:
        # Setup the api
        api = shodan.Shodan(API_KEY)

        fileToCheck = open(sys.argv[1],"r")
        noteable = []
        ips = []
        for line in fileToCheck:
                line.strip()
                parts = line.split(".")
                final = ".".join(parts[:-1])
                query = "ssl:"+line+" http.title:\"Openfire Admin Console\""
                print("Trying "+line)
                try:
                        result = api.search(query)
                except:
                        pass
                
                for service in result['matches']:
                        ips.append(str(service['ip_str']))
                        try:
                            discordMessage("Noteable: potential "+line+" at "+str(service['ip_str']))
                        except:
                                pass
                final = ".".join(parts[:-1])
                query = line+" http.title:\"Openfire Admin Console\""
                print("Trying "+line)
                try:
                        result = api.search(query)
                except:
                        pass
                
                for service in result['matches']:
                        ips.append(str(service['ip_str']))
                        try:
                            discordMessage("Noteable: potential "+line+" at "+str(service['ip_str']))
                        except:
                                pass
                if len(final.strip()) < 3:
                        pass
                else:
                        query = "ssl:"+line+" http.title:\"Openfire Admin Console\""
                time.sleep(2)
                try:
                        result = api.search(query)
                except:
                        pass
                for service in result['matches']:
                        if str(service['ip_str']) not in ips:
                                try:
                                    discordMessage("Noteable: potential "+line+" at "+str(service['ip_str']))
                                except:
                                        pass
        out = open("fireout.txt","w")
        for ip in noteable:
                out.write(str(ip))
except Exception as e:
        print('Error: %s' % e)
        sys.exit(1)
