"""a few overpass related functions"""

import os
import time
import json

import overpass
import osm2geojson
import geopandas as gpd

def run_overpass_query(
    query: str,
    retries: int = 3,
    op: overpass.API = None,
    cache_path: str = None,
    verbosity: str = "body"
) -> gpd.GeoDataFrame:
    """Safer wrapper for the overpass api, plus cacher"""
    if op is None:
        op = overpass.API()
    if os.path.isfile(cache_path):
        return gpd.read_file(cache_path)
    while retries:
        try:
            xml = op.get(query, responseformat="xml", verbosity=verbosity)
            print(f"Succesfully executed query..")
            break
        except Exception as e:
            print(f"Failed query due to {e}")
            retries -= 1
            if retries > 0:
                print(f"Failed on try {retries}, pausing 5 seconds before continuing")
                time.sleep(5)
                continue
            else:
                raise
    if cache_path:
        with open(cache_path, 'w') as f:
            json.dump(
                osm2geojson.xml2geojson(xml),
                f
            )
            print(f"Succesfully cached data {os.path.basename(cache_path)}")
        return gpd.read_file(cache_path)
    return xml