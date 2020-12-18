#!/usr/bin/env python3

# Check for infos in source
# Url is http://localhost:8888

# Library for opening url and creating  
# requests 
from urllib.request import urlopen
  
# pretty-print python data structures 
from pprint import pprint 
  
# for parsing all the tables present  
# on the website 
from html_table_parser import HTMLTableParser 
  
# for converting the parsed data in a 
# pandas dataframe 
import pandas as pd 

from http.server import BaseHTTPRequestHandler, HTTPServer
import time, re
from datetime import datetime

hostName = "localhost"
serverPort = 8888

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json; charset=utf-8")
        self.end_headers()
        
        # defining the html contents of a URL.
        # Get your stop from https://mobil.bvg.de/Fahrinfo/bin/stboard.bin/dox?
        # If you search for the stop you just get the schedule, so further click on "Haltestelleninfo" and in the link the stop number is coded
        # after ...dox?input=
        # Example link: https://mobil.bvg.de/Fahrinfo/bin/stboard.bin/dox?input=900160742&boardType=&time=20:33&productsFilter=1111111111111111&date=18.12.20&maxJourneys=&
        # now add the number here and ready to work
        xhtml = url_get_contents('https://mobil.bvg.de/Fahrinfo/bin/stboard.bin/dox?input=900160742&boardType=depRT&start=1').decode('utf-8') 
        # Defining the HTMLTableParser object 
        p = HTMLTableParser() 
          
        # feeding the html contents in the 
        # HTMLTableParser object 
        p.feed(xhtml) 


        now=datetime.now()
        depTime=datetime.now()

        start = '['
        for idx,item in enumerate(p.tables[0]):
            if idx == 0:
                #start = start + '[\"Linie\", \"Richtung\", \"Abf.\"],'
                None
            else:
                # This quick and dirty an works only if there is no construction or working site or something like this
                hh=int(p.tables[0][idx][0][0:2])
                mm=int(p.tables[0][idx][0][3:5])
                depTime=depTime.replace(hour=hh,minute=mm)
                if re.match(".*\*",p.tables[0][idx][0]):
                    minutes_diff='--'
                else:
                    minutes_diff = int((depTime - now).total_seconds() / 60)
                line = '[\"'+str(p.tables[0][idx][1])+'\",\"'+str(p.tables[0][idx][2])+'\",\"'+'('+str(minutes_diff)+') '+str(p.tables[0][idx][0])+'\"]'
                if idx < len(p.tables[0])-1:
                    start = start + line + ','
                else:
                    start = start + line + ']'

        self.wfile.write(bytes(start, "utf-8"))

# Opens a website and read its 
# binary contents (HTTP Response Body) 
def url_get_contents(url): 
    #making request to the website 
    f = urlopen(url=url)
    #reading contents of the website 
    return f.read() 

if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
