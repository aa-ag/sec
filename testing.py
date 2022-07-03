############------------ IMPORTS ------------###################################
import requests
import pandas as pd
from pprint import pprint


############------------ FUNCTION(S) ------------##############################
def get_ciks():
    url = "https://www.sec.gov/files/company_tickers.json"
    headers = {"User-Agent": "aaron@aguerrevere.dev"}
    http_request = requests.get(url, headers)
    response = http_request.json()
    
    df = pd.json_normalize(
        pd.json_normalize(
            response, max_level=0
        ).values[0]
    )
    print(df.head(3))


############------------ DRIVER CODE ------------##############################ß
get_ciks()