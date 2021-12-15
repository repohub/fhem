from http.server import BaseHTTPRequestHandler, HTTPServer
import re
from datetime import datetime

# Library for opening url and creating  
# requests 
from urllib.request import urlopen

#The only use of this helper is to convert the hafas rest api to simple httpmod json for fhem

# Now it is only available from localhost, to make it publicly available add external ip e.g. 192.168.78.3
hostName = "127.0.0.1"
serverPort = 8888

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json; charset=utf-8")
        self.end_headers()

        # use vbb rest api
        # 
        # for further information see https://v5.vbb.transport.rest/getting-started.html
        # e.g. 900134501 is the id of the station
        link = "https://v5.vbb.transport.rest/stops/900134501/departures?results=20&duration=60"

        f = urlopen(link)

        linenr = ""
        direction = ""
        when = ""
        plannedWhen = ""
        minutes_diff = ""
        result = ""
        i = 0
        itmp = 0

        now=datetime.now()
        depTime=datetime.now()

        line = f.readline()
        while line:
            ld = line.decode('utf-8')
            if re.search("nr",ld):
                linenr = ld.split(":")[1]
                linenr = linenr.replace(',','')
                linenr = linenr.strip()
            if re.search("direction",ld):
                direction = ld.split(":")[1]
                direction = direction.replace('"','')
                direction = direction.replace(',','')
                direction = direction.strip()
            if re.search("when",ld):
                when = ld.strip()
                when = when.split("T")[1]
                when = when.split("+")[0]
                when = when[0:5]
            if re.search("plannedWhen",ld):
                plannedWhen = ld.strip()
                plannedWhen = plannedWhen.split("T")[1]
                plannedWhen = plannedWhen.split("+")[0]
                hh = int(plannedWhen[0:2])
                mm = int(plannedWhen[3:5])
                depTime=depTime.replace(hour=hh,minute=mm)
                minutes_diff = int((depTime - now).total_seconds() / 60)
                #print(now)
                plannedWhen = plannedWhen[0:5]

            if re.search("tripId",ld):
                if i == 0:
                    result = '['
                else:
                    result = result+'[\"'+linenr+'\",\"'+direction+'\",\"'+'('+str(minutes_diff)+') '+when+'\"],'
                i = i + 1
            line = f.readline()
        f.close()
        result = result+'[\"'+linenr+'\",\"'+direction+'\",\"'+'('+str(minutes_diff)+') '+when+'\"]]'
        self.wfile.write(bytes(result, "utf-8"))

if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")


#Goal: 
# '[[\"line\", \"direction\", \"time\"],'
# ' [\"line\", \"direction\", \"time\"],'
# ' [\"line\", \"direction\", \"time\"]],'

'''
Example
[["50","Prenzlauer Berg, Björnsonstr.","(0) 21:09"],
["154","Buchholz-West, Aubertstr.","(7) 21:17"],
["50","Prenzlauer Berg, Björnsonstr.","(--) 21:20 *"],
["154","U Elsterwerdaer Platz","(10) 21:20"],
["50","Franz. Buchholz, Guyotstr.","(15) 21:25"]]
'''