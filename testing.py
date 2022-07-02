############------------ IMPORTS ------------###################################
import requests
from pprint import pprint


############------------ FUNCTION(S) ------------##############################
def get_ciks():
    url = 'https://www.sec.gove/files/company_tickets.json'
    http_request = requests.get(url)
    response = http_request.json()
    pprint(response)


############------------ DRIVER CODE ------------##############################ß
get_ciks()