from datetime import datetime
from fastapi import HTTPException
import googlemaps


class GeocoderService:

    def __init__(self, api_key):
        self.gmaps = googlemaps.Client(key=api_key)

    def input_json_converter(self, body):
        template = {
            "object": "null",
            "objectVersion": "null",
            "utcTimestamp": "null",
            "uuid": "null",
            "correlationId": "null",
            "statusCode": "null",
            "status": "null",
            "type": "null",
            "description": "null",
            "account": {
                "jobNumber": "null",
                "PortNumber": "null",  # (varchar(20)) Portfolio number
                "PortName": "null",  # (varchar(40)) Portfolio name
                "AccNumber": "null",  # (nvarchar(40)) Account number
                "AccName": "null",  # (nvarchar(100)) Account name
                "AccGroup": "null",
                # (varchar(40)) Account group, could use to group multiple accounts (e.g. for binders)
            },
            "location": {
                "addressee": "null",
                "unitNumber": "null",
                "civicNumber": "null",
                "StreetAddress": "null",  # nvarchar(100) Street address including house number
                "streetType": "null",
                "City": "null",  # (nvarchar(50)) City
                "AreaCode": "null",
                # (nvarchar(20)) Code representing typically the largest sub-division in a country (e.g. State code). See AreaCode Values sheet for details.
                "AreaName": "null",
                # (nvarchar(50)) Name relating to the AreaCode (e.g. State name). See AreaCode Values sheet for details.
                "PostalCode": "null",  # (nvarchar(20)) Postcode: the highest resolution postcode most often used
                "CountryCode": "null",  # (char(2)) Country code (based on ISO3166 alpha-2 codes)
                "countryName": "null",
                "AddressMatch": "null",
                # (tinyint) Address match from geocoder: indicating the resolution that the latitude / longitude represents
                "GeocodeQuality": "null",
                # (float) Geocode quality (values between 0 and 1 e.g. 80% is entered as 0.8)
                "Geocoder": "null",
                # (varchar(20)) Company name / version of geocoder. Free text field.
                "Longitude": "null",  # (decimal) Latitude in degrees (-90.0 to +90.0)
                "Latitude": "null",  # (decimal) Longitude in degrees (-180.0 to +180.0)
                "location_type": "null",
                "coordinateRefSystem": "null"
            },
            "information": {
                "OccupancyCode": "null",  # (tinyint) OED occupancy code
                "ConstructionCode": "null",  # (tinyint) OED construction code
                "YearBuilt": "null",  # (smallint) Year built (4 digit year)
                "NumberOfStoreys": "null",  # (tinyint) Number of storeys
                "FloorArea": "null",  # (float) Floor area: the total area across all floors
                "FloorAreaUnit": "null",  # (tinyint) Units in which FloorArea is specified
                "Basement": "null",
                # (tinyint) Code that defines if there is a basement and if so whether it is finished or unfinished
                "BasementLevelCount": "null",
                # (tinyint) Indicates the number of basement levels in a structure (supports up to 5 levels; for more than 5, enter 5).
                "FoundationType": "null",
                # (tinyint) Code that represents the construction type of the building's foundation
                "FirstFloorHeight": "null",
                # (float) Height of the lowest floor (above ground) of the building with respect to local ground elevation (NOT relative to datum). First floor in the US is identical to ground floor in Europe.
                "FirstFloorHeightUnit": "null",
                # (tinyint) Code for the unit of measure used to express FirstFloorHeight
                "GroundElevation": "null",
                # (float) Flood or Windstorm - Elevation of the local ground surface at the building at this location. This field represents the elevation of the grade (local ground surface) with respect to the datum (e.g. NAVD88).
                "GroundElevationUnit": "null",
                # (tinyint) Code for the unit of measure used to express the GroundElevation
                "BuildingHeight": "null",  # (float) Total height of the structure
                "BuildingHeightUnit": "null",  # (tinyint) Units of the BuildingHeight
                "BuildingType": "null",  # (tinyint) Building type (e.g. detached, terraced, etc)
            },
            "coverage": {
                "AccDedCode1Building": "null",  # (tinyint) Account building deductible code
                "AccDedType1Building": "null",  # (tinyint) Account building deductible type
                "AccDed1Building": "null",  # (float) Account building deductible
                "AccLimitCode1Building": "null",  # (tinyint) Account building limit code
                "AccLimitType1Building": "null",  # (tinyint) Account building limit type
                "AccLimit1Building": "null",  # (float) Account building limit
                "AccDedCode3Contents": "null",  # (tinyint) Account contents deductible code
                "AccDedType3Contents": "null",  # (tinyint) Account contents deductible type
                "AccDed3Contents": "null",  # (float) Account contents deductible
                "AccLimitCode3Contents": "null",  # (tinyint) Account contents limit code
                "AccLimitType3Contents": "null",  # (tinyint) Account contents limit type
                "AccLimit3Contents": "null",  # (float) Account contents limit
            },
            "financial": {
                "BuildingTIV": "null",  # (float) Building Total Insured Value
                "ContentsTIV": "null",  # (float) Content Total Insured Value
                "BITIV": "null"  # (float) Business Interruption (BI) Total Insured Value
            },
            "calculations": {
                "CorrelationGroup": "null",
                # (int) Correlation Group: indicates which location should be correlated between each other in Oasis LMF
                "BuildingID": "null",  # (varchar(20)) Unique building identification number
                "rpValues": "null",
                "hazardValues": "null",
                "aal": "null",
                "floodIndex": "null"
            }
        }

        if body['account'].get('jobNumber') is None:
            raise HTTPException(status_code=400, detail=f"Missing field: jobNumber")
        if body['location'].get('addressee') is None:
            raise HTTPException(status_code=400, detail=f"Missing field: addressee")
        if body['location'].get('StreetAddress') is None:
            raise HTTPException(status_code=400, detail=f"Missing field: StreetAddress")
        if body['location'].get('City') is None:
            raise HTTPException(status_code=400, detail=f"Missing field: City")
        if body['location'].get('province') is None:
            raise HTTPException(status_code=400, detail=f"Missing field: province")
        if body['location'].get('PostalCode') is None:
            raise HTTPException(status_code=400, detail=f"Missing field: PostalCode")
        if body['location'].get('country') is None:
            raise HTTPException(status_code=400, detail=f"Missing field: country")
        if body['financial'].get('BuildingTIV') is None:
            raise HTTPException(status_code=400, detail=f"Missing field: BuildingTIV")

        template['object'] = "input_json_converter-response"
        template['objectVersion'] = 1
        template['utcTimestamp'] = str(datetime.utcnow())
        template['statusCode'] = 200
        template['status'] = "ok"
        template['type'] = "Success"
        template['description'] = "The request has succeeded."
        template['account']['jobNumber'] = body['account'].get('jobNumber')
        template['location']['addressee'] = body['location'].get('addressee')
        template['location']['StreetAddress'] = body['location'].get('StreetAddress')
        template['location']['City'] = body['location'].get('City')
        template['location']['AreaName'] = body['location'].get('province')
        template['location']['PostalCode'] = body['location'].get('PostalCode')
        template['location']['countryName'] = body['location'].get('country')
        template['financial']['BuildingTIV'] = body['financial'].get('BuildingTIV')

        return template


    def geocoder(self, in_json):
        streetAddress = in_json['location'].get('StreetAddress')
        if streetAddress == "null":
            streetAddress = ""
        else:
            streetAddress = streetAddress + ", "

        unitNumber = in_json['location'].get('unitNumber')
        if unitNumber == "null":
            unitNumber = ""
        else:
            unitNumber = "unit " + str(unitNumber) + ", "

        city = in_json['location'].get('City')
        if city == "null":
            city = ""
        else:
            city = city + ", "

        province = in_json['location'].get('AreaName')
        if province == "null":
            province = ""
        else:
            province = province + ", "

        postalCode = in_json['location'].get('PostalCode')
        if postalCode == "null":
            postalCode = ""
        else:
            postalCode = postalCode + ", "

        country = in_json['location'].get('countryName')
        if country == "null":
            country = ""

        address = streetAddress + unitNumber + city + province + postalCode + country
        print("Geocoding address: ", address)

        result = self.gmaps.geocode(address=address, region='ca')
        in_json['object'] = "geocoder-response"
        in_json['objectVersion'] = 1
        in_json['utcTimestamp'] = str(datetime.utcnow())
        in_json['statusCode'] = 200
        in_json['status'] = "ok"
        in_json['type'] = "Success"
        in_json['description'] = "The request has succeeded."
        in_json['location']['Geocoder'] = "Google Geocoding API"
        in_json['location']['Longitude'] = result[0]['geometry']['location']['lng']
        in_json['location']['Latitude'] = result[0]['geometry']['location']['lat']
        in_json['location']['location_type'] = result[0]['geometry']['location_type']
        in_json['location']['coordinateRefSystem'] = "epsg4326"
        return in_json
