import sys
import json

def get_additions(list1, list2):
    """ Returns new calendar events """
    additions = [ x.strip('\n') for x in list2 if x not in list1]
    return additions

def get_deletions(list1, list2):
    """ Returns calendar events to be deleted """
    #calculate deletions
    deletions = [ x for x in list1 if x not in list2]
    return deletions
