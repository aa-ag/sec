############------------ IMPORTS ------------###################################
import requests
import pandas as pd
from pprint import pprint


############------------ FUNCTION(S) ------------##############################
def get_ciks(headers):
    url = "https://www.sec.gov/files/company_tickers.json"
    http_request = requests.get(url, headers=headers)
    response = http_request.json()
    
    df = pd.json_normalize(
        pd.json_normalize(
            response, max_level=0
        ).values[0]
    )

    df["cik_str"] = df["cik_str"].astype(str).str.zfill(10)
    df.set_index("title", inplace=True)

    df.to_csv("ciks.csv")


def get_company_facts(cik, headers):
    api = "https://data.sec.gov/api/xbrl/"
    endpoint = f"companyfacts/CIK{cik}.json"
    url = api + endpoint
    http_request = requests.get(url, headers=headers)
    print(http_request.status_code)



############------------ DRIVER CODE ------------##############################ß
if __name__ == "__main__":
    # get_ciks(headers)
    headers = {"User-Agent": "aaron@aguerrevere.dev"}
    get_company_facts("0000320193", headers)