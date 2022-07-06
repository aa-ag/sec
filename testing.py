############------------ IMPORTS ------------###################################
import requests
import pandas as pd
from pprint import pprint
import json


############------------ FUNCTION(S) ------------##############################
def get_ciks(headers):
    '''
     get ciks from sec & save them in a csv
    '''
    # set urls, headers & make a request
    url = "https://www.sec.gov/files/company_tickers.json"
    http_request = requests.get(url, headers=headers)
    response = http_request.json()
    
    # normalize the response json
    df = pd.json_normalize(
        pd.json_normalize(
            response, max_level=0
        ).values[0]
    )

    # fill each cik with zeroes to make sure each is 10 digits long
    df["cik_str"] = df["cik_str"].astype(str).str.zfill(10)
    # make "title" the index (left-most)
    df.set_index("title", inplace=True)
    # save the newly formatted dataframe into a csv
    df.to_csv("ciks.csv")


def get_company_facts(cik, headers):
    # set urls, headers & make a request
    api = "https://data.sec.gov/api/xbrl/"
    endpoint = f"companyfacts/CIK{cik}.json"
    url = api + endpoint
    http_request = requests.get(url, headers=headers)
    # format the response as a json
    response = http_request.json()
    # pretty-print the response
    pprint(response)


def get_company_financials(cik, headers):
    # set urls, headers & make a request
    api = "https://data.sec.gov/api/xbrl/"
    endpoint = f"companyconcept/CIK{cik}/us-gaap/Assets.json"
    url = api + endpoint
    http_request = requests.get(url, headers=headers)
    if http_request.status_code == 200:
        # format the response as a json
        response = http_request.json()
        # pretty-print the response
        pprint(response)
    else:
        print(f"Something's wrong.\nStatus code: {http_request.status_code}")


def get_company_submissions(cik, headers):
    # set urls, headers & make a request
    api = "https://data.sec.gov/"
    endpoint = f"submissions/CIK{cik}.json"
    url = api + endpoint
    http_request = requests.get(url, headers=headers)
    if http_request.status_code == 200:
        # format the response as a json
        response = http_request.json()
        # pretty-print the response
        store = open("submissions.json", "w")
        json.dump(response, store)
        print("All done.")
    else:
        print(f"Something's wrong.\nStatus code: {http_request.status_code}")


def get_forms():
    url = "https://www.sec.gov/forms"
    tables = pd.read_html(url)
    df = pd.concat(tables)

    forms = set()

    for i, row in df.iterrows():
        form_name = row["Number"].split(':')[1]
        forms.add(form_name)

    print(forms)


############------------ DRIVER CODE ------------##############################
if __name__ == "__main__":
    # get_ciks(headers)
    headers = {"User-Agent": "aaron@aguerrevere.dev"}
    # get_company_facts("0000320193", headers)
    # get_company_financials("0000320193", headers)
    # get_company_submissions("0001463172", headers)
    get_forms()