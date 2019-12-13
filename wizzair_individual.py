import requests
from datetime import datetime, timedelta
from tqdm import tqdm
import json
import pandas as pd
import pickle

# This is included in every query, I just stored them for the sake of simplicity
with open('services.json') as json_file:
    services = json.load(json_file)

headers = {
    'authority': 'be.wizzair.com',
    'accept': 'application/json, text/plain, */*',
    'origin': 'https://wizzair.com',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
    'content-type': 'application/json;charset=UTF-8',
    'sec-fetch-site': 'same-site',
    'sec-fetch-mode': 'cors',
    'referer': 'https://wizzair.com/',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-GB,en;q=0.9,hu-HU;q=0.8,hu;q=0.7,en-US;q=0.6'}

data = {"isFlightChange":False,
        "isSeniorOrStudent":False,
        "flightList":[{"departureStation":"BUD",
                       "arrivalStation":"TIA",
                       "departureDate":"2019-12-03"}],
        "adultCount":1,
        "childCount":0,
        "infantCount":0,
        "wdc":True}

arrival_stations = ["CRL", 
				"EIN", 
				"TLV", 
				"LTN", 
				"TIA", 
				"GYD", 
				"BRU", 
				"SJJ",
				"BOJ",
				"SOF",
				"LCA",
				"BOD",
				"NCE",
				"KUT",
			   "SXF",
			   "DTM",
			   "FRA",
			   "HAJ",
			   "ATH",
			   "CFU",
			   "HER",
			   "RHO",
			   "SKG",
			   "ZTH",
			   "KEF",
			   "ETM",
			   "AHO",
			   "BRI",
			   "BLQ",
			   "CTA",
			   "MXP",
			   "NAP",
			   "FCO",
			   "TSE",
			   "PRN",
			   "MLA",
			   "TGD",
			   "SKP",
			   "OSL",
			   "WAW",
			   "FAO",
			   "LIS",
			   "OPO",
			   "TGM",
			   "KZN",
			   "VKO",
			   "LED",
			   "ALC",
			   "BCN",
			   "CDT",
			   "IBZ",
			   "MAD",
			   "AGP",
			   "PMI",
			   "TFS",
			   "GOT",
			   "MMX",
			   "NYO",
			   "BSL",
			   "HRK",
			   "IEV",
			   "LWO",
			   "ODS",
			   "OZH",
			   "DWC",
			   "BHX",
			   "DSA",
			   "EDI",
			   "GLA",
			   "LPL",
			   "LGW"]
base = datetime.today() + timedelta(days = 1)
date_list = [base + timedelta(days=x) for x in range(170)]

data_list = []
for date in tqdm(date_list):
    data["flightList"][0]["departureDate"] = date.strftime("%Y-%m-%d")
    for arrival_station in arrival_stations:
        data["flightList"][0]["arrivalStation"] = arrival_station
        response = requests.post('https://be.wizzair.com/10.1.0/Api/search/search', headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            resp_data = response.json()
            if resp_data["returnFlights"] is not None:
                data_list.append(resp_data["returnFlights"])
            if resp_data["outboundFlights"] is not None:
                data_list.append(resp_data["outboundFlights"])
        else:
            pass
            #print("Wrong payload", data)

flat_list = [item for sublist in data_list for item in sublist]
with open('wizz_data_list_format_individual_approach.pkl', 'wb') as f:
    pickle.dump(flat_list, f)