from arcgis.gis import GIS
from arcgis.geocoding import geocode,batch_geocode
import yaml
from shapely.geometry import Point
import time
import pandas as pd
import requests

class GeocodingUtils:
    gis = None
    conv_batch_size = 100
    api_access_token = None
    config_file = None


    def __init__(self,config_file):
        self.config_file = config_file
        config = None
        with open(config_file,'r') as yaml_file:
            config = yaml.load(yaml_file, Loader=yaml.Loader)

        arcConf = config['arcgis']
        arcUserId = arcConf['user_id']
        arcPassword = arcConf['password']

        self.gis = GIS(username=arcUserId, password=arcPassword)

    def set_batch_size(self,size):
        """
        setting the batch size for each request to the server
        :param size:
        :return None
        """
        self.conv_batch_size = size

    def addressToLatLong(self,address):
        """
        geocoding an address into Latitude and Longitudes
        :param address:
        :return: Shapely.geometry.POINT
        """
        results = geocode(address=address)
        loc = results[0]['location']
        return Point(loc['x'], loc['y'])
    def addressColToLatLong(self,column):
        """
        geocode an entire column of addresses into LatLong coordinates
        :param column: pandas.Series
        :return: pandas.Series
        """
        tot_len = len(column)
        loc_dict = {}
        for batch_no in range(int(tot_len/self.conv_batch_size)+1):
            start_ind = batch_no*self.conv_batch_size
            stop_ind = (batch_no+1)*self.conv_batch_size
            for ind, loc in zip(column[start_ind:stop_ind].index, batch_geocode(list(column[start_ind:stop_ind]))):
                loc_dict[ind] = Point(loc['location']['x'], loc['location']['y'])
            time.sleep(10)
        return pd.Series(loc_dict)

    def set_api_access_token(self):
        """
        generate new API token for accessing the RESTful server
        reads the config.yaml file and sets the access token
        :return: None
        """
        config = None
        with open(self.config_file, 'r') as yaml_file:
            config = yaml.load(yaml_file, Loader=yaml.Loader)
            oauthUrl = config['oauthUrl']
            oauth_payload = config['arcAPICredentials']
            response = requests.request("POST", oauthUrl, data=oauth_payload)
            self.api_access_token = response.json()['access_token']

    def road_distance(self,start, dest):
        """
        calculates the road distance between two given points
        :param start: shapely.geometry.Point
        :param dest: shapely.geometry.Point
        :return: distance
        """
        req_payload = {}
        req_payload['f'] = 'json'
        req_payload['token'] = self.api_access_token
        req_payload['stops'] = "{start_x},{start_y};{dest_x},{dest_y}".format(start_x=start.x, start_y=start.y, dest_x=dest.x, dest_y=dest.y)

        headers = { 'content-type': "application/x-www-form-urlencoded" }

        api_url = "https://route.arcgis.com/arcgis/rest/services/World/Route/NAServer/Route_World/solve"

        route_response = requests.request("POST", api_url, data=req_payload, headers=headers)
        return route_response.json()['directions'][0]['summary']['totalLength']

