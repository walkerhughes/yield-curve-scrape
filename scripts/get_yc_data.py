import json
import requests
from datetime import datetime
from bs4 import BeautifulSoup

def get_current_month():
    today = datetime.today().date()
    year, month = today.year, today.month
    if month < 10:
        month = f"0{month}"
    return f"{year}{month}"

def format_payload_url():
    current_month = get_current_month()
    return f"https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?type=daily_treasury_yield_curve&field_tdr_date_value_month={current_month}"

def scrape_yield_curve_data_json():
    response = requests.get(format_payload_url())
    soup = BeautifulSoup(response.text, "html")
    yc_values_on_date = soup.find_all("tr")[-1]
    parsed_data = [_.text.strip() for _ in yc_values_on_date.__dict__["contents"][1::2]]
    yc_data_json = {
        "date": parsed_data[0],
        "one_mo": float(parsed_data[10]),
        "two_mo": float(parsed_data[11]),
        "three_mo": float(parsed_data[12]),
        "four_mo": float(parsed_data[13]),
        "six_mo": float(parsed_data[14]),
        "one_yr": float(parsed_data[15]),
        "two_yr": float(parsed_data[16]),
        "three_yr": float(parsed_data[17]),
        "five_yr": float(parsed_data[18]),
        "seven_yr": float(parsed_data[19]),
        "ten_yr": float(parsed_data[20]),
        "twenty_yr": float(parsed_data[21]),
        "thirty_yr": float(parsed_data[22]),
    }
    return yc_data_json, response.status_code

def get_yc_data(verbose = False):
    try:
        if verbose:
            print("Initiating attempt to retrieve Yield Curve data... ", end = " ")
        yc_data_json, status_code = scrape_yield_curve_data_json()
        if verbose:
            print(f"successful with status code {status_code}.")

        return yc_data_json
    except:
        raise ValueError(f"Failed with status code {status_code}. Either 'Month' argument invalid or data cannot be parsed as implemented.")

def save_to_json(dict_obj):
    date = dict_obj["date"].replace("/", "-")
    with open(f"./data/{date}.json", "w") as newfile:
        json.dump(dict_obj, newfile)
    print(f"File saved to ./data/{date}.json")
