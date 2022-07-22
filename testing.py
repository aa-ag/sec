############------------ IMPORTS ------------###################################
from email import header
import requests
import pandas as pd
from pprint import pprint
import json
import feedparser
import re
from bs4 import BeautifulSoup as bs
import xml.etree.ElementTree as ET
import webbrowser


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
        store = open("submissions.json", "w")
        json.dump(response, store)
        print("All done.")
    else:
        print(f"Something's wrong.\nStatus code: {http_request.status_code}")


def get_forms():
    '''
     read forms website, concatenate resulting
     list of dataframes and save the concatenated
     df into a csv store for reusing locally
    '''
    url = "https://www.sec.gov/forms"
    tables = pd.read_html(url)
    df = pd.concat(tables)

    df.to_csv('forms.csv')


def read_forms():
    '''
     read downloaded forms and return
     each form name
    '''
    df = pd.read_csv('forms.csv')

    forms = set()

    for i, row in df.iterrows():
        forms.add(row["Number"].split(':')[1])

    pprint(forms)


def parse_rss_feed():
    '''
     Parse ssf feed from SEC
    '''
    url = 'https://www.sec.gov/Archives/edgar/usgaap.rss.xml'
    feed = feedparser.parse(url, agent="User-Agent aaron@aguerrevere.dev")
    print(feed['entries'])
    # store = open("rss.json", "w")
    # json.dump(feed, store)
    # print("All done.")


def a_ten_k(url,count,headers):
    '''
     try to get specific doc: 10k for a given company
    '''
    r = requests.get(
        url,
        headers=headers
    )
    # print(r.status_code)
    data = r.text
    soup = bs(data[0:1300], 'lxml')
    
    with open(f'tesla_{count}.txt', 'w') as miso:
        miso.write(str(soup))

    
def parse_xml(headers):
    url = 'https://www.sec.gov/Archives/edgar/data/1463172/000146317222000098/wf-form4_165040006949831.xml'
    r = requests.get(
        url,
        headers=headers
    )

    # with open('xmltest.xml', 'w') as xmltest:
    #     xmltest.write(r.text)

    root = ET.fromstring(r.text)
    
    for element in root.iter():
        print(f"{element.tag}: {element.text}")


def test_submissions():
    submissions = open("submissions.json")
    data = json.load(submissions)
    return data
    

def get_past_ten_ks(cik, headers):
    # get_company_submissions(cik, headers)
    data = test_submissions()
    forms = data["filings"]["recent"]["form"]
    
    ten_ks = {"10-K's": []}

    for i in range(len(forms)):
        if forms[i] == '10-K':
            ten_ks["10-K's"].append(i)

    indices = ten_ks["10-K's"]
    accession_numbers = data["filings"]["recent"]["accessionNumber"]
    count = 1
    for i in indices:
        clean = accession_numbers[i].replace('-', '')
        url = f'https://www.sec.gov/Archives/edgar/data/{cik}/' + clean
        print(url)
        a_ten_k(url, count, headers)
        count += 1


def test_url_patterns():
    year = 2016
    while year < 2022:
        url = f'https://www.sec.gov/Archives/edgar/data/1318605/000156459017003118/tsla-10k_{year}1231.htm'
        year += 1
        webbrowser.open(url)

############------------ DRIVER CODE ------------##############################
if __name__ == "__main__":
    # get_ciks(headers)
    headers = {"User-Agent": "aaron@aguerrevere.dev"}
    # get_company_facts("0000320193", headers)
    # get_company_financials("0001463172", headers)
    # get_company_submissions("0001463172", headers)
    # get_forms()
    # read_forms()
    # parse_rss_feed()
    # a_ten_k(headers)
    # parse_xml(headers)
    # test_submissions()
    # get_past_ten_ks("0001318605", headers)
    test_url_patterns()