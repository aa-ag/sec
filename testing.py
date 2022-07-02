############------------ IMPORTS ------------###################################
from urllib.request import Request, urlopen


############------------ FUNCTION(S) ------------##############################
def get_data():
    cik = 'aapl'
    url = f'https://data.sec.gov/submissions/CIK{cik}.json'
    h = {"Accept": "application/json", "User-Agent": "Mozilla/5.0"}
    http_request = Request(url, headers=h)
    http_response = urlopen(http_request)
    print(http_response.status)


############------------ DRIVER CODE ------------##############################ß
get_data()