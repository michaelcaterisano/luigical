# USAGE: python csvToJson.py <infile> <outfile>

import csv
import json
import sys
import re
import pytz

from datetime import datetime

def get_formatted_events(event_list):
    """ Returns a list of events formatted as json for the google cal api """
    output = []
    errors = []
    rows = csv.reader(event_list)
    for row in rows:
        # skip header
        if row[0] == 'Subject' and row[1] == 'Start Date':
            continue
        # check to see if start date is later than end date
        # if so, append to errors[]
        if row[2] > row[4]:
            errors.append(row)
        # append remaining items to output array
        else:
            # calculate daylight savings time
            date_list = row[1].split('-')
            year = int(date_list[0])
            month = int(date_list[1])
            day = int(date_list[2])
            dst = bool(pytz.timezone('America/New_York').dst(datetime(year,month,day), is_dst=None))

            if dst:
                ext = ':00-04:00'
            else:
                ext = ':00-05:00'

            print('HEY!!!!!')
            print(dst)
            print(year, month, day)
            output.append({
                'summary': row[0],
                'description': row[6],
                'start':{
                    'dateTime': row[1] + 'T' + row[2] + ext,
                    'timeZone': 'America/New_York',
                },
                'end':{
                    'dateTime':row[3] + 'T' + row[4] + ext,
                    'timeZone': 'America/New_York',
                }
                })

        #if errors, append to errorfile
        with open('dockervolume/errorfile.txt', 'a+') as errorfile:
            if errors:
                for i in range(len(errors)):
                    json.dump(errors[i], errorfile)
                    errorfile.write(',' + '\n')

    return output
