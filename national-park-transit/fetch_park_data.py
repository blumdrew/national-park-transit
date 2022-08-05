"""Fetch data on all National Parks in a given region"""

from typing import Union
import os
import geopandas as gpd

from overpass_tools import run_overpass_query
from constants import BASE_PATH, QUERY_PATH, DATA_PATH

def fetch_transit_data(
    relation_id: int,
    output_location: os.PathLike = None
) -> Union[gpd.GeoDataFrame, None]:
    """Fetch transit data for park"""
    query_path = os.path.join(
        QUERY_PATH,
        "transit_routes_in_parks.op"
    )
    if relation_id == 1870066:
        query_path = os.path.join(
            QUERY_PATH,
            "transit_routes_in_parks_1870066.op"
        )
    with open(query_path, 'r') as f:
        query = f.read()
    query = query.format(relation_id)
    #print(query)
    cache_path = os.path.join(
        DATA_PATH,
        "transit_routes",
        f"transit_data_{relation_id}.geojson"
    )
    os.makedirs(os.path.dirname(cache_path),exist_ok=True)

    transit_data = run_overpass_query(
        query=query,
        cache_path=cache_path,
        #verbosity="geom"
    )
    if not transit_data.empty:
        return transit_data
    else:
        return gpd.GeoDataFrame(
            columns=["type","id","tags","geometry"]
        )

def fetch_park_data(
    country_name: str = "United States",
    cache_transit_data: bool = True
) -> gpd.GeoDataFrame:
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
        f"{country_name}_national_parks.geojson"
    )
    park_data = run_overpass_query(
        query=query,
        cache_path=cache_path,
        verbosity="geom"
    )
    park_data = park_data[park_data["type"]=="relation"]
    if not cache_transit_data:
        return park_data
    # fetch all potentially interesting transit routes and cache
    for idx in park_data.index:
        park = park_data.loc[idx]
        print(f"Fetching transit data for {park['tags'].get('name')}")
        park_id = park["id"]
        transit_data = fetch_transit_data(park_id)
        
    return park_data

if __name__ == "__main__":
    fetch_park_data()