"""(insert better description)"""
# TODO change filter on admin level to be > 6, rather than = 8
# imports
import os
from random import random
from typing import Optional, Sequence, Union

import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

from constants import OSM_NAME_ID_MAP, DATA_PATH, QUERY_PATH, OSM_ID_VISITOR_MAP
from fetch_park_data import fetch_park_data, fetch_transit_data
from overpass_tools import run_overpass_query

class Park(object):
    """insert description here"""
    def __init__(
        self,
        country_name: str,
        osm_relation_id: Optional[int] = None,
        park_name: Optional[str] = None
    ) -> None:
        self.country_name = country_name
        self.country_data_path = os.path.join(
            DATA_PATH,
            f"{country_name}_national_parks.geojson"
        )
        if not os.path.isfile(self.country_data_path):
            fetch_park_data(self.country_name)
        self.all_park_data = gpd.read_file(self.country_data_path)

        if not osm_relation_id and not park_name:
            raise ValueError("Must pass either park name or OSM relation ID")
        elif not osm_relation_id:
            self.park_name = park_name
            self.osm_relation_id = OSM_NAME_ID_MAP.get(self.park_name)
            if not self.osm_relation_id:
                raise KeyError(f"Unable to find park name {self.park_name} in mapped constants, please use OSM ID instead")
        elif not park_name:
            self.osm_relation_id = osm_relation_id
            osm_id_name_map = {value:key for key, value in zip(OSM_NAME_ID_MAP.keys(), OSM_NAME_ID_MAP.values())}
            self.park_name = osm_id_name_map.get(self.osm_relation_id)
        
        self.park_data = self.all_park_data[
            self.all_park_data["id"] == self.osm_relation_id
        ]
        if not self.park_name:
            self.park_name = self.park_data["tags"].apply(lambda x: x.get("name")).iloc[0]
        if self.park_data.empty:
            raise ValueError(f"OSM ID of {self.osm_relation_id} not found in park data for {self.country_name}")
        
        self.transit_data_path = os.path.join(
            DATA_PATH,
            "transit_routes",
            f"transit_data_{self.osm_relation_id}.geojson"
        )
        if not os.path.isfile(self.transit_data_path):
            self.transit_data = fetch_transit_data(self.osm_relation_id)
        else:
            self.transit_data = gpd.read_file(self.transit_data_path)
        if self.transit_data.empty:
            self.transit_stops = self.transit_data
        else:
            self.transit_stops = self.transit_data[
                self.transit_data["tags"].apply(lambda x: x.get("public_transport")).notnull()
                | (self.transit_data["tags"].apply(lambda x: x.get("route")) == "ferry")
            ]
        self.cities_served = self._fetch_cities_on_transit_routes()
        self.parking_lots = self._fetch_parking_lots()

        # forward declarations
        self._parking_lot_area = None
        self._park_area = None

    def _fetch_cities_on_transit_routes(
        self
    ) -> gpd.GeoDataFrame:
        """get all cities served by the transit routes in question"""
        if self.transit_data.empty:
            return gpd.GeoDataFrame(
                columns=["type","id","tags","geometry"]
            )
        query_path = os.path.join(
            QUERY_PATH,
            "cities_on_transit_route.op"
        )
        with open(query_path, 'r') as f:
            query = f.read()
        
        # loop over types
        all_cities = []
        for tp in ["node","way","relation"]:
            slc = self.transit_stops[
                self.transit_stops["type"] == tp
            ]
            if slc.empty:
                continue
            elif len(slc.index) == 1:
                id_string = str(slc["id"].iloc[0])
            else:
                id_string = "id:"+",".join(slc["id"].astype(str))
            tp_query = query.format(tp, id_string)
            cache_path = os.path.join(
                DATA_PATH,
                "cities_on_transit_routes",
                f"cities_served_{self.osm_relation_id}_{tp}.geojson"
            )
            os.makedirs(os.path.dirname(cache_path), exist_ok=True)
            cities_on_route_tp = run_overpass_query(
                tp_query,
                cache_path=cache_path,
                verbosity="geom"
            )
            if not cities_on_route_tp.empty:
                all_cities.append(cities_on_route_tp)
        if len(all_cities) > 0:
            all_cities = pd.concat(all_cities,ignore_index=True)
        else:
            all_cities = gpd.GeoDataFrame(
                columns=["type","id","tags","geometry"]
            )

        return all_cities
    
    def _fetch_parking_lots(self) -> gpd.GeoDataFrame:
        """Get parking lots within park too"""
        query_path = os.path.join(
            QUERY_PATH,
            "parking_lots.op"
        )
        cache_path = os.path.join(
            DATA_PATH,
            "parking_lots",
            f"parking_lots_{self.osm_relation_id}.geojson"
        )
        os.makedirs(os.path.dirname(cache_path),exist_ok=True)
        with open(query_path, 'r') as f:
            query = f.read()
        query = query.format(self.osm_relation_id)
        gdf = run_overpass_query(
            query=query,
            cache_path=cache_path
        )
        return gdf

    def plot_park(
        self,
        output_path: os.PathLike = None
    ) -> bool:
        """make a plot that looks good, shows cities served"""
        if not output_path:
            output_path = os.path.join(
                DATA_PATH,
                "images",
                f"{self.park_name} transit routes.png"
            )
        os.makedirs(os.path.dirname(output_path),exist_ok=True)
        if os.path.isfile(output_path):
            print(f"{output_path} exists, skipping")

        fig, ax = plt.subplots()

        ax.set_aspect('equal')
        ax.axis("off")

        # plot park, add label
        self.park_data.plot(ax=ax,color="#0b9f55")
        ax.annotate(self.park_name, (1,1), xycoords="figure points")

        # add transit data, if applicable
        if not self.transit_data.empty:
            self.transit_data.plot(
                ax=ax,
                color="black",
                alpha=0.5
            )
            # add city data too, if applicable
            if not self.cities_served.empty:
                self.cities_served.plot(
                    ax=ax,
                    cmap="viridis"
                )
                # annotate city locations
                for city_index in self.cities_served.index:
                    city = self.cities_served.loc[city_index]
                    city_name = city["tags"].get("name", "unknown city")
                    city_center = city["geometry"].centroid
                    ax.annotate(city_name,xy=(city_center.x, city_center.y),fontsize="small")
        else:
            return False
        plt.savefig(output_path, dpi=1_000)
        return True

    def parking_lot_area(
        self
    ) -> float:
        """return m^2 of parking lots, using UTM CRS"""
        if self._parking_lot_area is not None:
            return self._parking_lot_area
        if self.parking_lots.empty:
            self._parking_lot_area = 0
            return 0
        utm_crs = self.parking_lots.estimate_utm_crs()
        pl_merc = self.parking_lots.to_crs(crs=utm_crs)
        area = pl_merc["geometry"].area.sum()
        self._parking_lot_area = area
        return area

    def park_area(
        self
    ) -> float:
        """return m^2 of park, using UTM CRS"""
        if self._park_area is not None:
            return self._park_area
        utm_crs = self.park_data.estimate_utm_crs()
        pl_merc = self.park_data.to_crs(crs=utm_crs)
        area = pl_merc["geometry"].area.sum()
        self._park_area = area
        return area
    
    @property
    def number_of_parking_spaces(
        self
    ) -> int:
        """An estimate of the number of parking spaces provided
        in the park. Based on a 5m X 2.5m space, with 60% of 
        floor space in a lot dedicated to spaces."""
        return int((self.parking_lot_area() / (5*2.5)) * 0.5)
    
    @property
    def cities_served_by_transit(
        self
    ) -> Union[str, Sequence[str], None]:
        """"""
        if self.cities_served.empty:
            return None
        cities = self.cities_served["tags"].apply(lambda x: x.get("name")).values
        if len(cities) == 1:
            return cities[0]
        else:
            return cities

    @property
    def park_visitors(
        self
    ) -> int:
        """"""
        return OSM_ID_VISITOR_MAP.get(self.osm_relation_id,0)

if __name__ == "__main__":
    parks = gpd.read_file(os.path.join(DATA_PATH,"United States_national_parks.geojson"))
    parks = parks[parks["tags"].apply(lambda x: x.get("name","poop")).str.contains("National Park")]
    for park_id in parks["id"]:
        park = Park("United States", osm_relation_id=park_id)
        visitors_per_space = "NaN" if park.park_visitors == 0 else park.number_of_parking_spaces/(park.park_visitors/365)
        print(f"Park '{park.park_name}' has roughly {park.number_of_parking_spaces} parking spaces, and {park.park_visitors} visitors in 2021 for a total of {visitors_per_space} spaces per visitor per day")
        #print(f"Park '{park.park_name}' has direct transit connections to: {park.cities_served_by_transit}")
        
