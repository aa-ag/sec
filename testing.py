############------------ IMPORTS ------------###################################
from email import header
import requests
from pprint import pprint


############------------ FUNCTION(S) ------------##############################
def get_ciks():
    url = 'https://www.sec.gov/files/company_tickets.json'
    headers = {'User-Agent': 'aaron@aguerrevere.dev'}
    http_request = requests.get(url, headers=headers)
    response = http_request.json()
    pprint(response)


############------------ DRIVER CODE ------------##############################ß
get_ciks()