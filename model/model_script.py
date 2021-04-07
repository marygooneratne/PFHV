import pandas as pd
_HOMES = './data/homes_complete.csv'
_HISTORY = './data/history_complete.csv'
_NATIONAL = "./data/macro_national.csv"
_REGIONAL = "./data/macro_regional.csv"
_ZIPCODE = "./data/macro_zipcode.csv"
_REGIONS = "./data/regions.csv"
_ZIPCODE_TO_REGION ="./zipcode_to_region.csv"

def macro_data(zipcode, year):
    data = {
        "zipcode_rating": None,
        "rgl_housing_starts": None,
        "rgl_new_home_sales": None,
        "ntl_construction_spending": None,
        "ntl_housing_starts": None,
        "ntl_home_sales": None,
        "ntl_housing_price_idx": None
    }
    national_df = pd.read_csv(_NATIONAL)
    regional_df = pd.read_csv(_REGIONAL)
    zipcode_df = pd.read_csv(_ZIPCODE)
    regions_df = pd.read_csv(_REGIONS)
    zipcode_to_region_df = pd.read_csv(_ZIPCODE_TO_REGION)