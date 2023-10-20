import typing
from http import client

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel

from app.service.geocoder_service import GeocoderService
from app.service.mediator_service import MediatorService
import os
import json
from fastapi_cloudauth.cognito import Cognito
import app.Utils as utils

auth = Cognito(
    region=utils.COGNITO_region,
    userPoolId=utils.COGNITO_userPoolId,
    client_id=utils.COGNITO_client_id
)


class AccessUser(BaseModel):
    sub: str


api_key = os.environ.get('GCP_API_KEY')

geocoderService = GeocoderService(api_key)
mediatorService = MediatorService()

router = APIRouter()


class JsonConverterInput(BaseModel):
    object: str
    account: dict
    location: dict
    financial: dict

    class Config:
        schema_extra = {
            "example": {
                # User request example
                "object": "client-request",
                "account": {
                    "jobNumber": "0123456789"
                },
                "location": {
                    "addressee": "John Doe Inc.",
                    "unitNumber": None,
                    "StreetAddress": "2964 De La Riviere Nelson St",
                    "City": "Quebec",
                    "province": "Quebec",
                    "PostalCode": "G2A 1A2",
                    "country": "Canada"
                },
                "financial": {
                    "BuildingTIV": 1000000
                }
            }
        }


class GeocoderInput(BaseModel):
    object: str
    objectVersion: int
    utcTimestamp: str
    uuid: str
    correlationId: str
    statusCode: int
    status: str
    type: str
    description: str
    correlationId: str
    account: dict
    location: dict
    information: dict
    coverage: dict
    financial: dict
    calculations: dict

    class Config:
        schema_extra = {
            "example": {
                "object": "input_json_converter-response",
                "objectVersion": 1,
                "utcTimestamp": "2023-09-21 05:05:36.166304",
                "uuid": "null",
                "correlationId": "null",
                "statusCode": 200,
                "status": "ok",
                "type": "Success",
                "description": "The request has succeeded.",
                "account": {
                    "jobNumber": "0123456789",
                    "PortNumber": "null",
                    "PortName": "null",
                    "AccNumber": "null",
                    "AccName": "null",
                    "AccGroup": "null"
                },
                "location": {
                    "addressee": "John Doe Inc.",
                    "unitNumber": "null",
                    "civicNumber": "null",
                    "StreetAddress": "2964 De La Riviere Nelson St",
                    "streetType": "null",
                    "City": "Quebec",
                    "AreaCode": "null",
                    "AreaName": "Quebec",
                    "PostalCode": "G2A 1A2",
                    "CountryCode": "null",
                    "countryName": "Canada",
                    "AddressMatch": "null",
                    "GeocodeQuality": "null",
                    "Geocoder": "null",
                    "Longitude": "null",
                    "Latitude": "null",
                    "location_type": "null",
                    "coordinateRefSystem": "null"
                },
                "information": {
                    "OccupancyCode": "null",
                    "ConstructionCode": "null",
                    "YearBuilt": "null",
                    "NumberOfStoreys": "null",
                    "FloorArea": "null",
                    "FloorAreaUnit": "null",
                    "Basement": "null",
                    "BasementLevelCount": "null",
                    "FoundationType": "null",
                    "FirstFloorHeight": "null",
                    "FirstFloorHeightUnit": "null",
                    "GroundElevation": "null",
                    "GroundElevationUnit": "null",
                    "BuildingHeight": "null",
                    "BuildingHeightUnit": "null",
                    "BuildingType": "null"
                },
                "coverage": {
                    "AccDedCode1Building": "null",
                    "AccDedType1Building": "null",
                    "AccDed1Building": "null",
                    "AccLimitCode1Building": "null",
                    "AccLimitType1Building": "null",
                    "AccLimit1Building": "null",
                    "AccDedCode3Contents": "null",
                    "AccDedType3Contents": "null",
                    "AccDed3Contents": "null",
                    "AccLimitCode3Contents": "null",
                    "AccLimitType3Contents": "null",
                    "AccLimit3Contents": "null"
                },
                "financial": {
                    "BuildingTIV": 1000000,
                    "ContentsTIV": "null",
                    "BITIV": "null"
                },
                "calculations": {
                    "CorrelationGroup": "null",
                    "BuildingID": "null",
                    "rpValues": "null",
                    "hazardValues": "null",
                    "aal": "null",
                    "floodIndex": "null"
                }
            }
        }


class HazardExtractionInput(BaseModel):
    object: str
    objectVersion: int
    utcTimestamp: str
    uuid: str
    correlationId: str
    statusCode: int
    status: str
    type: str
    description: str
    correlationId: str
    account: dict
    location: dict
    information: dict
    coverage: dict
    financial: dict
    calculations: dict

    class Config:
        schema_extra = {
            "example": {
                "object": "geocoder-response",
                "objectVersion": 1,
                "utcTimestamp": "2023-09-21 05:07:29.399482",
                "uuid": "null",
                "correlationId": "null",
                "statusCode": 200,
                "status": "ok",
                "type": "Success",
                "description": "The request has succeeded.",
                "account": {
                    "jobNumber": "0123456789",
                    "PortNumber": "null",
                    "PortName": "null",
                    "AccNumber": "null",
                    "AccName": "null",
                    "AccGroup": "null"
                },
                "location": {
                    "addressee": "John Doe Inc.",
                    "unitNumber": "null",
                    "civicNumber": "null",
                    "StreetAddress": "2964 De La Riviere Nelson St",
                    "streetType": "null",
                    "City": "Quebec",
                    "AreaCode": "null",
                    "AreaName": "Quebec",
                    "PostalCode": "G2A 1A2",
                    "CountryCode": "null",
                    "countryName": "Canada",
                    "AddressMatch": "null",
                    "GeocodeQuality": "null",
                    "Geocoder": "Google Geocoding API",
                    "Longitude": -71.37819,
                    "Latitude": 46.86871319999999,
                    "location_type": "ROOFTOP",
                    "coordinateRefSystem": "epsg4326"
                },
                "information": {
                    "OccupancyCode": "null",
                    "ConstructionCode": "null",
                    "YearBuilt": "null",
                    "NumberOfStoreys": "null",
                    "FloorArea": "null",
                    "FloorAreaUnit": "null",
                    "Basement": "null",
                    "BasementLevelCount": "null",
                    "FoundationType": "null",
                    "FirstFloorHeight": "null",
                    "FirstFloorHeightUnit": "null",
                    "GroundElevation": "null",
                    "GroundElevationUnit": "null",
                    "BuildingHeight": "null",
                    "BuildingHeightUnit": "null",
                    "BuildingType": "null"
                },
                "coverage": {
                    "AccDedCode1Building": "null",
                    "AccDedType1Building": "null",
                    "AccDed1Building": "null",
                    "AccLimitCode1Building": "null",
                    "AccLimitType1Building": "null",
                    "AccLimit1Building": "null",
                    "AccDedCode3Contents": "null",
                    "AccDedType3Contents": "null",
                    "AccDed3Contents": "null",
                    "AccLimitCode3Contents": "null",
                    "AccLimitType3Contents": "null",
                    "AccLimit3Contents": "null"
                },
                "financial": {
                    "BuildingTIV": 1000000,
                    "ContentsTIV": "null",
                    "BITIV": "null"
                },
                "calculations": {
                    "CorrelationGroup": "null",
                    "BuildingID": "null",
                    "rpValues": "null",
                    "hazardValues": "null",
                    "aal": "null",
                    "floodIndex": "null"
                }
            }
        }


class LossCalculationInput(BaseModel):
    object: str
    objectVersion: int
    utcTimestamp: str
    uuid: str
    correlationId: str
    statusCode: int
    status: str
    type: str
    description: str
    correlationId: str
    account: dict
    location: dict
    information: dict
    coverage: dict
    financial: dict
    calculations: dict

    class Config:
        schema_extra = {
            "example": {
                "object": "hazard-extraction-response",
                "objectVersion": 1,
                "utcTimestamp": "2023-09-21 05:11:41.700207",
                "uuid": "null",
                "correlationId": "null",
                "statusCode": 200,
                "status": "ok",
                "type": "Success",
                "description": "The request has succeeded.",
                "account": {
                    "jobNumber": "0123456789",
                    "PortNumber": "null",
                    "PortName": "null",
                    "AccNumber": "null",
                    "AccName": "null",
                    "AccGroup": "null"
                },
                "location": {
                    "addressee": "John Doe Inc.",
                    "unitNumber": "null",
                    "civicNumber": "null",
                    "StreetAddress": "2964 De La Riviere Nelson St",
                    "streetType": "null",
                    "City": "Quebec",
                    "AreaCode": "null",
                    "AreaName": "Quebec",
                    "PostalCode": "G2A 1A2",
                    "CountryCode": "null",
                    "countryName": "Canada",
                    "AddressMatch": "null",
                    "GeocodeQuality": "null",
                    "Geocoder": "Google Geocoding API",
                    "Longitude": -71.37819,
                    "Latitude": 46.86871319999999,
                    "location_type": "ROOFTOP",
                    "coordinateRefSystem": "epsg4326"
                },
                "information": {
                    "OccupancyCode": "null",
                    "ConstructionCode": "null",
                    "YearBuilt": "null",
                    "NumberOfStoreys": "null",
                    "FloorArea": "null",
                    "FloorAreaUnit": "null",
                    "Basement": "null",
                    "BasementLevelCount": "null",
                    "FoundationType": "null",
                    "FirstFloorHeight": "null",
                    "FirstFloorHeightUnit": "null",
                    "GroundElevation": "null",
                    "GroundElevationUnit": "null",
                    "BuildingHeight": "null",
                    "BuildingHeightUnit": "null",
                    "BuildingType": "null"
                },
                "coverage": {
                    "AccDedCode1Building": "null",
                    "AccDedType1Building": "null",
                    "AccDed1Building": "null",
                    "AccLimitCode1Building": "null",
                    "AccLimitType1Building": "null",
                    "AccLimit1Building": "null",
                    "AccDedCode3Contents": "null",
                    "AccDedType3Contents": "null",
                    "AccDed3Contents": "null",
                    "AccLimitCode3Contents": "null",
                    "AccLimitType3Contents": "null",
                    "AccLimit3Contents": "null"
                },
                "financial": {
                    "BuildingTIV": 1000000,
                    "ContentsTIV": "null",
                    "BITIV": "null"
                },
                "calculations": {
                    "CorrelationGroup": "null",
                    "BuildingID": "null",
                    "rpValues": [
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
                    ],
                    "hazardValues": [
                        0,
                        0,
                        0,
                        0,
                        9,
                        10,
                        15,
                        20,
                        28,
                        35,
                        42,
                        46
                    ],
                    "aal": "null",
                    "floodIndex": "null"
                }
            }
        }


class FloodIndexInput(BaseModel):
    object: str
    objectVersion: int
    utcTimestamp: str
    uuid: str
    correlationId: str
    statusCode: int
    status: str
    type: str
    description: str
    correlationId: str
    account: dict
    location: dict
    information: dict
    coverage: dict
    financial: dict
    calculations: dict

    class Config:
        schema_extra = {
            "example": {
                "object": "loss-calculation-response",
                "objectVersion": 1,
                "utcTimestamp": "2023-09-21 05:12:44.538245",
                "uuid": "null",
                "correlationId": "null",
                "statusCode": 200,
                "status": "ok",
                "type": "Success",
                "description": "The request has succeeded.",
                "account": {
                    "jobNumber": "0123456789",
                    "PortNumber": "null",
                    "PortName": "null",
                    "AccNumber": "null",
                    "AccName": "null",
                    "AccGroup": "null"
                },
                "location": {
                    "addressee": "John Doe Inc.",
                    "unitNumber": "null",
                    "civicNumber": "null",
                    "StreetAddress": "2964 De La Riviere Nelson St",
                    "streetType": "null",
                    "City": "Quebec",
                    "AreaCode": "null",
                    "AreaName": "Quebec",
                    "PostalCode": "G2A 1A2",
                    "CountryCode": "null",
                    "countryName": "Canada",
                    "AddressMatch": "null",
                    "GeocodeQuality": "null",
                    "Geocoder": "Google Geocoding API",
                    "Longitude": -71.37819,
                    "Latitude": 46.86871319999999,
                    "location_type": "ROOFTOP",
                    "coordinateRefSystem": "epsg4326"
                },
                "information": {
                    "OccupancyCode": "null",
                    "ConstructionCode": "null",
                    "YearBuilt": "null",
                    "NumberOfStoreys": "null",
                    "FloorArea": "null",
                    "FloorAreaUnit": "null",
                    "Basement": "null",
                    "BasementLevelCount": "null",
                    "FoundationType": "null",
                    "FirstFloorHeight": "null",
                    "FirstFloorHeightUnit": "null",
                    "GroundElevation": "null",
                    "GroundElevationUnit": "null",
                    "BuildingHeight": "null",
                    "BuildingHeightUnit": "null",
                    "BuildingType": "null"
                },
                "coverage": {
                    "AccDedCode1Building": "null",
                    "AccDedType1Building": "null",
                    "AccDed1Building": "null",
                    "AccLimitCode1Building": "null",
                    "AccLimitType1Building": "null",
                    "AccLimit1Building": "null",
                    "AccDedCode3Contents": "null",
                    "AccDedType3Contents": "null",
                    "AccDed3Contents": "null",
                    "AccLimitCode3Contents": "null",
                    "AccLimitType3Contents": "null",
                    "AccLimit3Contents": "null"
                },
                "financial": {
                    "BuildingTIV": 1000000,
                    "ContentsTIV": "null",
                    "BITIV": "null"
                },
                "calculations": {
                    "CorrelationGroup": "null",
                    "BuildingID": "null",
                    "rpValues": [
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
                    ],
                    "hazardValues": [
                        0,
                        0,
                        0,
                        0,
                        9,
                        10,
                        15,
                        20,
                        28,
                        35,
                        42,
                        46
                    ],
                    "aal": 2959,
                    "floodIndex": "null"
                }
            }
        }


@router.post("/input_json_converter", name='Input Json Converter')
async def input_json_converter(jsonConverterInput: JsonConverterInput, current_user: AccessUser = Depends(auth.claim(AccessUser))):
# async def input_json_converter(jsonConverterInput: JsonConverterInput):
    """
    - **location**: The location data to be converted. This parameter should include relevant location details for the Mediator API processing. (required)
    - **financial**: The financial data to be converted. This parameter should include relevant financial information required by the Mediator API for accurate analysis and processing. (required)
    """
    resp = geocoderService.input_json_converter(json.loads(jsonConverterInput.json()))
    return resp


@router.post("/geocoder", name='Geocoder')
async def geocoder(geocoderInput: GeocoderInput, current_user: AccessUser = Depends(auth.claim(AccessUser))):
# async def geocoder(geocoderInput: GeocoderInput):
    """
    - **location**: The location data to be converted. This parameter should include relevant location details for the Mediator API processing. (required)
    """
    resp = geocoderService.geocoder(json.loads(geocoderInput.json()))
    return resp


@router.post("/hazard_extraction", name='Hazard Extraction')
async def hazard_extraction(body: HazardExtractionInput, current_user: AccessUser = Depends(auth.claim(AccessUser))):
# async def hazard_extraction(body: HazardExtractionInput):
    """
    - **Longitude**: The longitude coordinate representing the location for which you want to extract hazard information. This parameter specifies the east-west position on the Earth's surface. (required)
    - **Latitude**: The latitude coordinate representing the location for which you want to extract hazard information. This parameter specifies the north-south position on the Earth's surface. (required)
    """
    resp = mediatorService.hazard_extraction(json.loads(body.json()))
    return resp


@router.post("/loss_calculation", name='Loss Calculation')
async def loss_calculation(body: LossCalculationInput, current_user: AccessUser = Depends(auth.claim(AccessUser))):
# async def loss_calculation(body: LossCalculationInput):
    """
    - **BuildingTIV**: The Total Insurable Value (TIV) of the building or property for which you want to calculate potential losses. This parameter represents the financial value of the structure. (required)
    - **hazardValues**: The water depth values associated with the specific location, serving as a measure of flood severity. These values are used to quantify the potential impact of flooding on the building. (required)
    """
    resp = mediatorService.loss_calculation(json.loads(body.json()))
    return resp


@router.post("/flood_index", name='Flood Index')
async def flood_index(body: FloodIndexInput, current_user: AccessUser = Depends(auth.claim(AccessUser))):
# async def flood_index(body: FloodIndexInput):
    """
    - **hazardValues**: The water depth values associated with the specific location, serving as a measure of flood severity. These values are used to quantify the potential impact of flooding on the building. (required)
    """
    resp = mediatorService.flood_index(json.loads(body.json()))
    return resp


@router.post("/single_building_query", name='Single Building Query')
async def single_building_query(body: JsonConverterInput, current_user: AccessUser = Depends(auth.claim(AccessUser))):
# async def single_building_query(body: JsonConverterInput):
    """
    - **location**: The location data to be converted. This parameter should include relevant location details for the Mediator API processing. (required)
    - **financial**: The financial data to be converted. This parameter should include relevant financial information required by the Mediator API for accurate analysis and processing. (required)
    """
    # input_json_converter
    out_json_converter = geocoderService.input_json_converter(json.loads(body.json()))
    # geocoder
    out_geocoder = geocoderService.geocoder(out_json_converter)
    # hazard_extraction
    out_hazard_extraction = mediatorService.hazard_extraction(out_geocoder)
    # loss_calculation
    out_loss_calculation = mediatorService.loss_calculation(out_hazard_extraction)
    # flood_index (need to fix when hazrdValues = 0)
    out_flood_index = mediatorService.flood_index(out_loss_calculation)
    return out_flood_index
