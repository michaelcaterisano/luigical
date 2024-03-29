# USAGE: python csvToJson.py <infile> <outfile>

import csv
import json
import sys
import re
import pytz
import pprint

from datetime import datetime

pp = pprint.PrettyPrinter()

def get_formatted_events(event_list):
    """ Returns a list of events formatted as json for the google cal api """
    output = []
    errors = []
    oldstuff = []
    rows = csv.reader(event_list)
    for row in rows:
        if row:
            # skip header
            if row[0] == 'Subject' and row[1] == 'Start Date':
                continue
            # check to see if start date is later than end date
            # if so, append to errors[]
            if row[2] > row[4]:
                errors.append(row)
            # append remaining items to output array
            elif not bool(re.search('(2015)|(2016)', row[1])):
                output.append({
                    'summary': row[0],
                    'description': row[6],
                    'start':{
                        'dateTime': row[1] + 'T' + row[2] + ':00',
                        'timeZone': 'America/New_York',
                    },
                    'end':{
                        'dateTime':row[3] + 'T' + row[4] + ':00',
                        'timeZone': 'America/New_York',
                    }
                    })

            # if errors, append to errorfile
            with open('dockervolume/errorfile.txt', 'a+') as errorfile:
                if errors:
                    for i in range(len(errors)):
                        json.dump(errors[i], errorfile)
                        errorfile.write(',' + '\n')
    # pp.pprint(errors)
    # pp.pprint(output)

    return output
