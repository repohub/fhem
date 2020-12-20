#!/bin/bash

# helper script to generate ics files from BSR Berlin and ALBA Berlin, Germany

mm=$(date +"%m")
yy=$(date +"%y")

## ALBA Berlin, Germany
#
# Using Firefox plugin HTTP Headers to obtain link
# Link can be retrieved by https://berlin.alba.info/service/abfallkalender/abfuhrtermine/
# add your Data and press "Export PDF file"
# Link:
#   https://api.abfall.io/?key=9583a2fa1df97ed95363382c73b41b1b&modus=d6c5855a62cf32a4dadbc2831f0f295f&waction=export_pdf
# Data:
#   f_id_kommune=3227&f_id_bezirk=1&f_qry_strasse=Prenz&f_posts_json[]=a:5:{s:12:"f_id_kommune";s:4:"3227";s:11:"f_id_bezirk";s:1:"1";s:13:"f_qry_strasse";s:5:"Prenz";s:12:"f_posts_json";a:0:{}s:12:"f_id_strasse";s:1:"0";},a:5:{s:12:"f_id_kommune";s:4:"3227";s:11:"f_id_bezirk";s:1:"1";s:13:"f_qry_strasse";s:5:"Prenz";s:12:"f_posts_json";a:0:{}s:12:"f_id_strasse";s:28:"3227prenzlauerpromenade13089";},a:6:{s:12:"f_id_kommune";s:4:"3227";s:11:"f_id_bezirk";s:1:"1";s:13:"f_qry_strasse";s:5:"Prenz";s:12:"f_posts_json";a:1:{i:0;s:151:"a:5:{s:12:"f_id_kommune";s:4:"3227";s:11:"f_id_bezirk";s:1:"1";s:13:"f_qry_strasse";s:5:"Prenz";s:12:"f_posts_json";a:0:{}s:12:"f_id_strasse";s:1:"0";}";}s:12:"f_id_strasse";s:28:"3227prenzlauerpromenade13089";s:16:"f_id_strasse_hnr";s:6:"264605";}&f_id_strasse=3227prenzlauerpromenade13089&f_id_strasse_hnr=264605&f_id_abfalltyp_0=19&f_id_abfalltyp_1=127&f_abfallarten_index_max=2&f_abfallarten=19,127&f_zeitraum=20200101-20201231&f_export_als={'action':'https://api.abfall.io/?key=9583a2fa1df97ed95363382c73b41b1b&modus=d6c5855a62cf32a4dadbc2831f0f295f&waction=export_pdf','target':'_blank'}
# 
# Now create your Link by changing export_pdf to export_ics in link and data. 
# Further escape the " by \"
# and remove in the end of data >>>,'target':'_blank'<<<
#   f_id_kommune=3227&f_id_bezirk=1&f_qry_strasse=Prenz&f_posts_json[]=a:5:{s:12:\"f_id_kommune\";s:4:\"3227\";s:11:\"f_id_bezirk\";s:1:\"1\";s:13:\"f_qry_strasse\";s:5:\"Prenz\";s:12:\"f_posts_json\";a:0:{}s:12:\"f_id_strasse\";s:1:\"0\";},a:5:{s:12:\"f_id_kommune\";s:4:\"3227\";s:11:\"f_id_bezirk\";s:1:\"1\";s:13:\"f_qry_strasse\";s:5:\"Prenz\";s:12:\"f_posts_json\";a:0:{}s:12:\"f_id_strasse\";s:28:\"3227prenzlauerpromenade13089\";},a:6:{s:12:\"f_id_kommune\";s:4:\"3227\";s:11:\"f_id_bezirk\";s:1:\"1\";s:13:\"f_qry_strasse\";s:5:\"Prenz\";s:12:\"f_posts_json\";a:1:{i:0;s:151:\"a:5:{s:12:\"f_id_kommune\";s:4:\"3227\";s:11:\"f_id_bezirk\";s:1:\"1\";s:13:\"f_qry_strasse\";s:5:\"Prenz\";s:12:\"f_posts_json\";a:0:{}s:12:\"f_id_strasse\";s:1:\"0\";}\";}s:12:\"f_id_strasse\";s:28:\"3227prenzlauerpromenade13089\";s:16:\"f_id_strasse_hnr\";s:6:\"264605\";}&f_id_strasse=3227prenzlauerpromenade13089&f_id_strasse_hnr=264605&f_id_abfalltyp_0=19&f_id_abfalltyp_1=127&f_abfallarten_index_max=2&f_abfallarten=19,127&f_zeitraum=20200101-20201231&f_export_als={'action':'https://api.abfall.io/?key=9583a2fa1df97ed95363382c73b41b1b&modus=d6c5855a62cf32a4dadbc2831f0f295f&waction=export_pdf','target':'_blank'}
#   
# ALBA does not provide data to curl bots, therefore we add a random client:
#   -A "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:78.0) Gecko/20100101 Firefox/78.0"
#
# The result looks like this (working example)
#   curl -skL "https://api.abfall.io/?key=9583a2fa1df97ed95363382c73b41b1b&modus=d6c5855a62cf32a4dadbc2831f0f295f&waction=export_ics" -A "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:78.0) Gecko/20100101 Firefox/78.0" --data-raw "f_id_kommune=3227&f_id_bezirk=1&f_qry_strasse=Pre&f_posts_json[]=a:5:{s:12:\"f_id_kommune\";s:4:\"3227\";s:11:\"f_id_bezirk\";s:1:\"1\";s:13:\"f_qry_strasse\";s:5:\"Pre\";s:12:\"f_posts_json\";a:0:{}s:12:\"f_id_strasse\";s:1:\"0\";},a:5:{s:12:\"f_id_kommune\";s:4:\"3227\";s:11:\"f_id_bezirk\";s:1:\"1\";s:13:\"f_qry_strasse\";s:5:\"Pre\";s:12:\"f_posts_json\";a:0:{}s:12:\"f_id_strasse\";s:28:\"3227prenzlauerpromenade13089\";},a:6:{s:12:\"f_id_kommune\";s:4:\"3227\";s:11:\"f_id_bezirk\";s:1:\"1\";s:13:\"f_qry_strasse\";s:5:\"Pre\";s:12:\"f_posts_json\";a:1:{i:0;s:151:\"a:5:{s:12:\"f_id_kommune\";s:4:\"3227\";s:11:\"f_id_bezirk\";s:1:\"1\";s:13:\"f_qry_strasse\";s:5:\"Pre\";s:12:\"f_posts_json\";a:0:{}s:12:\"f_id_strasse\";s:1:\"0\";}\";}s:12:\"f_id_strasse\";s:28:\"3227prenzlauerpromenade13089\";s:16:\"f_id_strasse_hnr\";s:6:\"264605\";}&f_id_strasse=3227prenzlauerpromenade13089&f_id_strasse_hnr=264605&f_id_abfalltyp_0=19&f_id_abfalltyp_1=127&f_abfallarten_index_max=2&f_abfallarten=19,127&f_zeitraum=20200101-20201231&f_export_als={'action':'https://api.abfall.io/?key=9583a2fa1df97ed95363382c73b41b1b&modus=d6c5855a62cf32a4dadbc2831f0f295f&waction=export_ics'}" > /tmp/alba.ics
# 
# For portability in years I added $yy in the linkdata part
# 
curl -skL "https://api.abfall.io/?key=9583a2fa1df97ed95363382c73b41b1b&modus=d6c5855a62cf32a4dadbc2831f0f295f&waction=export_ics" -A "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:78.0) Gecko/20100101 Firefox/78.0" --data-raw "f_id_kommune=3227&f_id_bezirk=1&f_qry_strasse=Pre&f_posts_json[]=a:5:{s:12:\"f_id_kommune\";s:4:\"3227\";s:11:\"f_id_bezirk\";s:1:\"1\";s:13:\"f_qry_strasse\";s:5:\"Pre\";s:12:\"f_posts_json\";a:0:{}s:12:\"f_id_strasse\";s:1:\"0\";},a:5:{s:12:\"f_id_kommune\";s:4:\"3227\";s:11:\"f_id_bezirk\";s:1:\"1\";s:13:\"f_qry_strasse\";s:5:\"Pre\";s:12:\"f_posts_json\";a:0:{}s:12:\"f_id_strasse\";s:28:\"3227prenzlauerpromenade13089\";},a:6:{s:12:\"f_id_kommune\";s:4:\"3227\";s:11:\"f_id_bezirk\";s:1:\"1\";s:13:\"f_qry_strasse\";s:5:\"Pre\";s:12:\"f_posts_json\";a:1:{i:0;s:151:\"a:5:{s:12:\"f_id_kommune\";s:4:\"3227\";s:11:\"f_id_bezirk\";s:1:\"1\";s:13:\"f_qry_strasse\";s:5:\"Pre\";s:12:\"f_posts_json\";a:0:{}s:12:\"f_id_strasse\";s:1:\"0\";}\";}s:12:\"f_id_strasse\";s:28:\"3227prenzlauerpromenade13089\";s:16:\"f_id_strasse_hnr\";s:6:\"264605\";}&f_id_strasse=3227prenzlauerpromenade13089&f_id_strasse_hnr=264605&f_id_abfalltyp_0=19&f_id_abfalltyp_1=127&f_abfallarten_index_max=2&f_abfallarten=19,127&f_zeitraum=20"$yy"0101-20"$yy"1231&f_export_als={'action':'https://api.abfall.io/?key=9583a2fa1df97ed95363382c73b41b1b&modus=d6c5855a62cf32a4dadbc2831f0f295f&waction=export_ics'}" > /tmp/alba.ics


## BSR Berlin
#
# Same as above, use Firefox plugin HTTP Headers to obtain links and information
# BSR uses a couple of ajax request which are fully played in order to get the needed information.

# Step 0: get cookie
curl -sL -c /tmp/c.txt "https://www.bsr.de/abfuhrkalender-20520.php" >> /dev/null

# Step 1: Search street, get json with matches (result can be ignored, use answer from HTTP Headers)
answer=$(curl -sL -b /tmp/c.txt "https://www.bsr.de/abfuhrkalender_ajax.php?script=dynamic_search&step=1&q=Pasewalker" | grep -c "value")
# better preserve the existing file, than overwriting
if [ 0 -eq "$answer" ]
then
    rm /tmp/c.txt
    exit 0
fi

# Step 2: Search the house number in the street from former matches in json file (result can be ignored, use answer from HTTP Headers)
curl -sL -b /tmp/c.txt "https://www.bsr.de/abfuhrkalender_ajax.php?script=dynamic_search&step=2&q=Pasewalker%20Str.,%2013127%20Berlin%20(Pankow)" >> /dev/null

# Step 3: Get garbage collection dates html style (working example)
# curl -sL -b /tmp/c.txt "https://www.bsr.de/abfuhrkalender_ajax.php?script=dynamic_kalender_ajax" --data-raw "abf_strasse=Pasewalker Str.&abf_hausnr=115&tab_control=Liste&abf_config_weihnachtsbaeume=&abf_config_restmuell=on&abf_config_biogut=on&abf_config_wertstoffe=on&abf_config_laubtonne=on&abf_selectmonth=12 2020&abf_datepicker=01.12.2020&listitems=7" >> /dev/null
# replace month and year again
curl -sL -b /tmp/c.txt "https://www.bsr.de/abfuhrkalender_ajax.php?script=dynamic_kalender_ajax" --data-raw "abf_strasse=Pasewalker Str.&abf_hausnr=115&tab_control=Liste&abf_config_weihnachtsbaeume=&abf_config_restmuell=on&abf_config_biogut=on&abf_config_wertstoffe=on&abf_config_laubtonne=on&abf_selectmonth=$mm 20$yy&abf_datepicker=01.$mm.20$yy&listitems=7" >> /dev/null

# Step 4: Download ics data (working example)
# curl -sL -b /tmp/c.txt "https://www.bsr.de/abfuhrkalender_ajax.php?script=dynamic_iCal_ajax&abf_strasse=Prenzlauer%20Promenade,%2013189%20Berlin%20(Pankow)&abf_hausnr=101&tab_control=Liste&abf_config_weihnachtsbaeume=&abf_config_restmuell=on&abf_config_biogut=on&abf_config_wertstoffe=on&abf_config_laubtonne=on&abf_selectmonth=12%202020&listitems=14" > /tmp/bsr.ics
# replace month and year again (be aware %20 is url coding)
curl -sL -b /tmp/c.txt "https://www.bsr.de/abfuhrkalender_ajax.php?script=dynamic_iCal_ajax&abf_strasse=Prenzlauer%20Promenade,%2013189%20Berlin%20(Pankow)&abf_hausnr=101&tab_control=Liste&abf_config_weihnachtsbaeume=&abf_config_restmuell=on&abf_config_biogut=on&abf_config_wertstoffe=on&abf_config_laubtonne=on&abf_selectmonth=$mm%2020$yy&listitems=14" > /tmp/bsr.ics

# cleanup
rm /tmp/c.txt
