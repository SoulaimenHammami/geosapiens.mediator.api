import os
import boto3
import mercantile
import numpy as np
import pandas as pd
from fastapi import HTTPException
from datetime import datetime
from rio_tiler.io import rasterio
from rioxarray import rioxarray
from scipy.interpolate import PchipInterpolator

HAZUS_DAMAGE_CURVE_CSV = os.environ.get('HAZUS_DAMAGE_CURVE_CSV')


class MediatorService:
    def __init__(self):
        pass

    def hazard_extraction(self, in_json):
        # Get tile coordinates
        lat = in_json['location']['Latitude']
        lon = in_json['location']['Longitude']
        # List of tiles that client has access
        tile_list = [(1235, 1442, 12)]
        # lat = 46.86765374437611
        # lon = -71.38526266153784
        # lat = 46
        # lon = -76

        if not is_location_in_tile(lat, lon, tile_list):
            raise HTTPException(status_code=403, detail=f"Location (lat: {lat}°, lon: {lon}°) is not within the current subscription area.")

        # Your code for a valid location goes here
        # zoom = 10
        # tile = mercantile.tile(lon, lat, zoom)
        # x, y = tile.x, tile.y
        #
        # # AWS file
        # session = boto3.Session()
        # s3_bucket = 'titiler'
        # s3_key = '1m_z10_v2/10_%s_%s_1.tif' % (x, y)
        # # s3_key = '30m_z10_v2/10_%s_%s_30.tif' % (x, y)
        # s3_url = f's3://{s3_bucket}/{s3_key}'

        ############# Demo ################
        # AWS file
        session = boto3.Session()
        s3_bucket = 'titiler-mediator-demo'
        s3_key = '12_1235_1442_1.tif'
        s3_url = f's3://{s3_bucket}/{s3_key}'
        ###################################

        # Extract data
        # try:
        cog_data = rioxarray.open_rasterio(s3_url, s3=session)
        # except rasterio.errors.RasterioIOError:
        #     raise CustomRasterIOError(s3_url)

        in_json['object'] = "hazard-extraction-response"
        in_json['objectVersion'] = 1
        in_json['utcTimestamp'] = str(datetime.utcnow())
        in_json['statusCode'] = 200
        in_json['status'] = "ok"
        in_json['type'] = "Success"
        in_json['description'] = "The request has succeeded."

        in_json['calculations']['rpValues'] = [
            2,
            5,
            10,
            20,
            25,
            50,
            100,
            150,
            200,
            500,
            1000,
            1500
        ]
        hazard_list = cog_data.sel(x=lon, y=lat, method='nearest').values.tolist()
        in_json['calculations']['hazardValues'] = [0 if x == 65535 else x for x in hazard_list]

        return in_json

    def loss_calculation(self, in_json):
        depth = pd.DataFrame(in_json['calculations']['hazardValues'], columns=['Depth'])
        # depth = pd.DataFrame(in_json["hazardValues"], columns=['Depth'])
        quantile = pd.DataFrame(
            [0.500000, 0.800000, 0.900000, 0.950000, 0.960000, 0.980000, 0.986667, 0.990000, 0.995000, 0.998000,
             0.999000, 0.999333], columns=['Quantile'])
        events = np.random.uniform(low=0.0, high=1.0, size=10000)

        TIV = in_json['financial']['BuildingTIV']

        vulnerability = pd.read_csv(HAZUS_DAMAGE_CURVE_CSV)  # read from db table via building property and location
        vulnerability_interp = PchipInterpolator(vulnerability['depth_m'], vulnerability['damage'], extrapolate=True)

        y = depth['Depth'] / 100  # when all depths = 0 aal=10% of TIV
        x = quantile['Quantile']
        set_interp = PchipInterpolator(x, y, extrapolate=True)
        edepth = set_interp(events)
        edamage = vulnerability_interp(edepth)
        eloss = edamage * TIV
        # Loss['RPloss'] = np.quantile(eloss, Loss['Quantile'])

        in_json['object'] = "loss-calculation-response"
        in_json['objectVersion'] = 1
        in_json['utcTimestamp'] = str(datetime.utcnow())
        in_json['statusCode'] = 200
        in_json['status'] = "ok"
        in_json['type'] = "Success"
        in_json['description'] = "The request has succeeded."

        in_json['calculations']['aal'] = int(np.mean(eloss))
        return in_json

    def flood_index(self, in_json):

        RP = np.array(in_json['calculations']['rpValues'])
        quantile = 1.0 - 1.0 / RP
        RPdepth = np.array(in_json['calculations']['hazardValues'])
        if np.all(RPdepth == 0):
            index = 0
        else:
            last_zero_index = np.max(np.where(RPdepth == 0))
            quantile = quantile[last_zero_index:len(RP)]
            RPdepth = RPdepth[last_zero_index:len(RP)]

            set_interp = PchipInterpolator(RPdepth, quantile, extrapolate=True)
            q1 = set_interp(0.5)

            years = 10

            prob = 1 - q1 ** years
            index = np.round(prob * 10)

        in_json['object'] = "flood-index-response"
        in_json['objectVersion'] = 1
        in_json['utcTimestamp'] = str(datetime.utcnow())
        in_json['statusCode'] = 200
        in_json['status'] = "ok"
        in_json['type'] = "Success"
        in_json['description'] = "The request has succeeded."

        in_json['calculations']['floodIndex'] = index

        return in_json


# class CustomRasterIOError(Exception):
#     def __init__(self, file_path):
#         self.file_path = file_path
#
#     def __str__(self):
#         return f"Error: File not found or could not be opened, the area is probably not covered. Please try another address. - '{self.file_path}'."
#
#
# class LocationNotInTileError(Exception):
#     # def __init__(self, lat, lon, tile_list):
#     def __init__(self, lat, lon):
#         self.lat = lat
#         self.lon = lon
#         # self.tile_list = tile_list
#         super().__init__(f"Error: Location ({lat}, {lon}) is not within the covered area.")


def is_location_in_tile(lat, lon, tile_list):
    location_tile = mercantile.tile(lon, lat, zoom=12)  # Adjust the zoom level as needed

    if location_tile in [(x, y, zoom) for x, y, zoom in tile_list]:
        return True
    return False
