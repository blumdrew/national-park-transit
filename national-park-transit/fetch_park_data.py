"""Fetch data on all National Parks in a given region"""

import os
import geopandas as gpd
from overpass_tools import run_overpass_query

BASE_PATH = os.path.dirname(__file__)
QUERY_PATH = os.path.join(BASE_PATH, "queries")
DATA_PATH = os.path.join(BASE_PATH, "data")

def fetch_park_data(
    country_name: str = "United States",
    output_location: os.PathLike = None
) -> bool:
    """only US for now"""
    if country_name != "United States":
        raise NotImplementedError("Only support for US National Parks for now")

    query_path = os.path.join(
        QUERY_PATH,
        "national_parks.op"
    )
    with open(query_path, 'r') as f:
        query = f.read()
    cache_path = os.path.join(
        DATA_PATH,
        "united_states_national_parks.geojson"
    )
    park_data = run_overpass_query(
        query=query,
        cache_path=cache_path
    )

    # process into a simpler, regular pandas df without geom data too
    print(park_data)

if __name__ == "__main__":
    fetch_park_data()