import uuid
from urllib.request import Request

import uvicorn

from fastapi import HTTPException

from mangum import Mangum
from fastapi import FastAPI
from app.routes import client_rest_router
from app.routes import mediator_router
from app.routes import auth_router
from app.monitoring import logging_config
from app.middlewares.correlation_id_middleware import CorrelationIdMiddleware
from app.middlewares.logging_middleware import LoggingMiddleware
from app.handlers.exception_handler import exception_handler
from app.handlers.http_exception_handler import http_exception_handler
from app.service import run
from app.Utils import * 

###############################################################################
#   Application object                                                        #
###############################################################################
description = """
Fetch required information from Geosapiens flood model for your critical business processes. Geosapiens Mediator API is 
a highly available automated service used for live analytics purposes and acting as a middleman between your automated 
systems and Geosapiens data layers. Given a set of inputs, it delivers all outputs required to compute a premium for a 
given risk. 

## Geosapiens Auth API
* **Login**: Allows secure access to the Geosapiens Mediator API. By providing valid credentials, users can obtain an 
authentication token. This token serves as a digital key, granting access to other API endpoints. It plays a crucial
 role in ensuring the security and integrity of your interactions with Geosapiens services.
\n

## Mediator API

* **Input Json Converter**: A component that streamlines your interaction with the Mediator API. It takes user-specific 
input data and transforms it into a format compatible with the Mediator API. This step ensures seamless data exchange 
and compatibility between your application and the Mediator API, simplifying the integration process.
\n
* **Geocoder**: Plays a pivotal role in spatial data processing. It takes location descriptions, such as addresses, and 
performs geocoding, which converts these descriptions into precise spatial coordinates. This spatial information is 
essential for accurately assessing flood risk and is particularly valuable from an underwriting perspective.
\n
* **Hazard Extraction**: Provides valuable insights into flood risk assessment. It categorizes flood depths based on 
their estimated hydrological return periods. This information is critical for understanding the severity of potential 
flooding scenarios, aiding in decision-making processes related to risk mitigation and insurance underwriting.
\n
* **Loss Calculation**:A tool for risk assessment that computes the Average Annual Loss (AAL) by utilizing flood depths 
and various risk characteristics. AAL is a key metric in risk management, enabling informed decisions on insurance 
premiums, risk mitigation strategies, and overall financial planning.
\n
* **Flood Index**: Designed to evaluate the severity of flooding events. It calculates a flood index based on the 
provided flood depths. This index provides a quantitative measure of flood severity, aiding in the prioritization of 
response efforts, resource allocation, and disaster preparedness. 
\n
* **Single Building Query**: Empowers you to perform a comprehensive data retrieval operation in a single request. It 
combines the capabilities of multiple API components, including geocoding, hazard extraction, loss calculation, and 
flood index computation, into a single, efficient query. This approach minimizes the number of requests required and 
optimizes your application's performance while obtaining detailed flood risk information for specific buildings or 
locations.
"""

app = FastAPI(title="Geosapiens Mediator API",
              description=description,
              version="1.0.0"
              )
"""
# Whitelisted IPs
WHITELISTED_IPS = ['165.231.251.156','188.241.176.37','88.138.238.159', '127.0.0.1']

@app.middleware('http')
async def validate_ip(request: Request, call_next):
    # Get client IP
    ip = str(request.client.host)

    # Check if IP is allowed
    if ip not in WHITELISTED_IPS:
        data = {
            'message': f'IP {ip} is not allowed to access this resource.'
        }
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=data)

    # Proceed if IP is allowed
    return await call_next(request)
"""

###############################################################################
#   Running db migrations                                                     #
###############################################################################
run()
###############################################################################
#   Logging configuration                                                     #
###############################################################################

logging_config.configure_logging(level='DEBUG', service='Mediator service', instance=str(uuid.uuid4()))

###############################################################################
#   Error handlers configuration                                              #
###############################################################################

app.add_exception_handler(Exception, exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)

###############################################################################
#   Middlewares configuration                                                 #
###############################################################################

# Tip : middleware order : CorrelationIdMiddleware > LoggingMiddleware -> reverse order
app.add_middleware(LoggingMiddleware)
app.add_middleware(CorrelationIdMiddleware)

###############################################################################
#   Routers configuration                                                     #
###############################################################################

app.include_router(auth_router.router, prefix='/auth', tags=['Geosapiens Auth API'])
app.include_router(mediator_router.router, prefix='/mediator', tags=['Mediator API'])
app.include_router(client_rest_router.router, prefix='/client', tags=['hello'])
###############################################################################
#   Handler for AWS Lambda                                                    #
###############################################################################

handler = Mangum(app)

###############################################################################
#   Run the self contained application                                        #
###############################################################################

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
