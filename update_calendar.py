import csvDiff
import csvToJson2
import luigiCalUpdate2
# import sys
# import os
# import json
# import CreateCredentials

def main():
    # Take old and new calendar csv files as arguments and store their contents in variables in list format
    with open('temp/oldcal.csv') as f:
        lines = f.readlines()
        previous_cal_events = [ line.strip('\n') for line in lines ]

    with open('temp/newcal.csv') as f:
        lines = f.readlines()
        new_cal_events = [ line.strip('\n') for line in lines]

    # Calculate event additions and deletions
    additions_list = csvDiff.get_additions(previous_cal_events, new_cal_events)
    deletions_list = csvDiff.get_deletions(previous_cal_events, new_cal_events)

    # Convert to Google event JSON format
    events_to_add = csvToJson2.get_formatted_events(additions_list)
    events_to_delete = csvToJson2.get_formatted_events(deletions_list)

    # Upload to Google Calendar
    luigiCalUpdate2.update_calendar(events_to_add, events_to_delete)

if __name__ == "__main__": main()
