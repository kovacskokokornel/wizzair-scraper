import requests
from datetime import datetime, timedelta
import pandas as pd
from tqdm import tqdm
import json
import sys

# This is to set the payload to each price type.
def alter_price(price_type, flights):
	if price_type == "wdc":
		[flight.update({"priceType": "wdc"}) for flight in flights]
	else:
		[flight.update({"priceType": "regular"}) for flight in flights]
	return flights

headers = {
	'authority': 'be.wizzair.com',
	'accept': 'application/json, text/plain, */*',
	'origin': 'https://wizzair.com',
	'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
	'content-type': 'application/json;charset=UTF-8',
	'sec-fetch-site': 'same-site',
	'sec-fetch-mode': 'cors',
	'referer': 'https://wizzair.com/en-gb/flights/timetable',
	'accept-encoding': 'gzip, deflate, br',
	'accept-language': 'en-GB,en;q=0.9,hu-HU;q=0.8,hu;q=0.7,en-US;q=0.6'}

# If you need data other than Budapest:
data = {"flightList":[{"departureStation":"BUD", # Change this
					   "arrivalStation":"",
					   "from":"",
					   "to":""},
					  {"departureStation":"",
					   "arrivalStation":"BUD", # and this
					   "from":"",
					   "to":""}],"priceType":"","adultCount":1,"childCount":0,"infantCount":0}

# These were collected by hand from the wizzair website, because I couldn't download them with code.
# The other airport is always Budapest as defined in the payload.
destinations = ["CRL", 
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

data_list = []
base = datetime.today()
# Here you can set how many periods you want to download (period = 42 days)
for period in range(6):
	# Only a maximum of 42 days is supported by wizzair.
	data["flightList"][0]["from"] = (base + timedelta(days = period * 42)).strftime("%Y-%m-%d")
	data["flightList"][1]["from"] = (base + timedelta(days = period * 42)).strftime("%Y-%m-%d")

	data["flightList"][0]["to"] = (base + timedelta(days = (period + 1) * 42)).strftime("%Y-%m-%d")
	data["flightList"][1]["to"] = (base + timedelta(days = (period + 1) * 42)).strftime("%Y-%m-%d")
	for price_type in ["regular", "wdc"]:
		data["priceType"] = price_type
		print(f"Downloading started with the following params for all destinations: {period}, {price_type}")
		for destination in tqdm(destinations):
			data["flightList"][0]["arrivalStation"] = destination
			data["flightList"][1]["departureStation"] = destination
			
			response = requests.post('https://be.wizzair.com/10.1.0/Api/search/timetable', headers=headers, data=json.dumps(data))
			if response.status_code == 200:
				data_list.append(alter_price(price_type, response.json()["outboundFlights"]))
				data_list.append(alter_price(price_type, response.json()["returnFlights"]))
			else:
				print("HTTP status: ", response.status_code)
				print("Something went wrong with this payload: ", data)

flat_list = [item for sublist in data_list for item in sublist]
df = pd.DataFrame(flat_list)

# It is better to have these in different columns
df["currencyCode"] = [x["currencyCode"] for x in df["price"]]
df["price"] = [x["amount"] for x in df["price"]]

# Writing it to a pickle file.
df.to_pickle("./wizzair_timetable_data.pkl")